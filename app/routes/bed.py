
from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Bed
from app.classes.forms import BedForm
from flask_login import login_required
import datetime as dt

@app.route('/bed/list')
@app.route('/beds')
# This means the user must be logged in to see this page
@login_required
def bedList():
    # This retrieves all of the 'blogs' that are stored in MongoDB and places them in a
    # mongoengine object as a list of dictionaries name 'blogs'.
    beds = Bed.objects()
    # This renders (shows to the user) the blogs.html template. it also sends the blogs object 
    # to the template as a variable named blogs.  The template uses a for loop to display
    # each blog.
    return render_template('beds.html',beds=beds)

# This route will get one specific blog and any comments associated with that blog.  
# The blogID is a variable that must be passsed as a parameter to the function and 
# can then be used in the query to retrieve that blog from the database. This route 
# is called when the user clicks a link on bloglist.html template.
# The angle brackets (<>) indicate a variable. 
@app.route('/bed/<bedID>')
# This route will only run if the user is logged in.
@login_required
def bed(bedID):
    # retrieve the blog using the blogID
    thisBed = Bed.objects.get(id=bedID)
    # If there are no comments the 'comments' object will have the value 'None'. Comments are 
    # related to blogs meaning that every comment contains a reference to a blog. In this case
    # there is a field on the comment collection called 'blog' that is a reference the Blog
    # document it is related to.  You can use the blogID to get the blog and then you can use
    # the blog object (thisBlog in this case) to get all the comments.
    # Send the blog object and the comments object to the 'blog.html' template.
    return render_template('bed.html',bed=thisBed,)

# This route will delete a specific blog.  You can only delete the blog if you are the author.
# <blogID> is a variable sent to this route by the user who clicked on the trash can in the 
# template 'blog.html'. 
# TODO add the ability for an administrator to delete blogs. 
@app.route('/bed/delete/<bedID>')
# Only run this route if the user is logged in.
@login_required
def bedDelete(bedID):
    # retrieve the blog to be deleted using the blogID
    deleteBed = Bed.objects.get(id=bedID)
    # check to see if the user that is making this request is the author of the blog.
    # current_user is a variable provided by the 'flask_login' library.
    if current_user == deleteBed.author:
        # delete the blog using the delete() method from Mongoengine
        deleteBed.delete()
        # send a message to the user that the blog was deleted.
        flash('The Bed was deleted.')
    else:
        # if the user is not the author tell them they were denied.
        flash("You can't delete a Bed you don't own.")
    # Retrieve all of the remaining blogs so that they can be listed.
    beds = Bed.objects()  
    # Send the user to the list of remaining blogs.
    return render_template('beds.html',beds=beds)

# This route actually does two things depending on the state of the if statement 
# 'if form.validate_on_submit()'. When the route is first called, the form has not 
# been submitted yet so the if statement is False and the route renders the form.
# If the user has filled out and succesfully submited the form then the if statement
# is True and this route creates the new blog based on what the user put in the form.
# Because this route includes a form that both gets and blogs data it needs the 'methods'
# in the route decorator.
@app.route('/bed/new', methods=['GET', 'POST'])
# This means the user must be logged in to see this page
@login_required
# This is a function that is run when the user requests this route.
def bedNew():
    # This gets the form object from the form.py classes that can be displayed on the template.
    form = BedForm()

    # This is a conditional that evaluates to 'True' if the user submitted the form successfully.
    # validate_on_submit() is a method of the form object. 
    if form.validate_on_submit():

        # This stores all the values that the user entered into the new blog form. 
        # Blog() is a mongoengine method for creating a new blog. 'newBlog' is the variable 
        # that stores the object that is the result of the Blog() method.  
        newBed = Bed(
            # the left side is the name of the field from the data table
            # the right side is the data the user entered which is held in the form object.
            BedLength = form.BedLength.data,
            BedWidth = form.BedWidth.data,
            MatressType = form.MatressType.data,
            BedSize = form.BedSize.data,
            author = current_user.id,

        )
        # This is a method that saves the data to the mongoDB database.
        newBed.save()

        # Once the new blog is saved, this sends the user to that blog using redirect.
        # and url_for. Redirect is used to redirect a user to different route so that 
        # routes code can be run. In this case the user just created a blog so we want 
        # to send them to that blog. url_for takes as its argument the function name
        # for that route (the part after the def key word). You also need to send any
        # other values that are needed by the route you are redirecting to.
        return redirect(url_for('bed',bedID=newBed.id))

    # if form.validate_on_submit() is false then the user either has not yet filled out
    # the form or the form had an error and the user is sent to a blank form. Form errors are 
    # stored in the form object and are displayed on the form. take a look at blogform.html to 
    # see how that works.
    return render_template('bedform.html',form=form)


# This route enables a user to edit a blog.  This functions very similar to creating a new 
# blog except you don't give the user a blank form.  You have to present the user with a form
# that includes all the values of the original blog. Read and understand the new blog route 
# before this one. 
@app.route('/bed/edit/<bedID>', methods=['GET', 'POST'])
@login_required
def bedEdit(bedID):
    editBed = Bed.objects.get(id=bedID)
    # if the user that requested to edit this blog is not the author then deny them and
    # send them back to the blog. If True, this will exit the route completely and none
    # of the rest of the route will be run.
    if current_user != editBed.author:
        flash("You can't edit a blog you don't own.")
        return redirect(url_for('bed',bedID=bedID))
    # get the form object
    form = BedForm()
    # If the user has submitted the form then update the blog.
    if form.validate_on_submit():
        # update() is mongoengine method for updating an existing document with new data.
        editBed.update(
            BedLength = form.BedLength.data,
            BedWidth = form.BedWidth.data,
            MatressType = form.MatressType.data,
            BedSize = form.BedSize.data,
        )
        # After updating the document, send the user to the updated blog using a redirect.
        return redirect(url_for('bed',bedID=bedID))

    # if the form has NOT been submitted then take the data from the editBlog object
    # and place it in the form object so it will be displayed to the user on the template.
    form.BedLength.data = editBed.BedLength
    form.BedWidth.data = editBed.Bedwid
    form.MatressType.data = editBed.MatressType
    form.BedSize.data = editBed.BedSize



    # Send the user to the blog form that is now filled out with the current information
    # from the form.
    return render_template('bedform.html',form=form)
