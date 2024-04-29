from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Workout
from app.classes.forms import WorkoutForm
from flask_login import login_required
import datetime as dt

# This is the route to list all blogs
@app.route('/workout/list')
@app.route('/workouts')
# This means the user must be logged in to see this page
@login_required
def workouts():
    # This retrieves all of the 'blogs' that are stored in MongoDB and places them in a
    # mongoengine object as a list of dictionaries name 'blogs'.
    workouts = Workout.objects()
    # This renders (shows to the user) the blogs.html template. it also sends the blogs object 
    # to the template as a variable named blogs.  The template uses a for loop to display
    # each blog.
    return render_template('workouts.html',workouts=workouts)

# This route will get one specific blog and any comments associated with that blog.  
# The blogID is a variable that must be passsed as a parameter to the function and 
# can then be used in the query to retrieve that blog from the database. This route 
# is called when the user clicks a link on bloglist.html template.
# The angle brackets (<>) indicate a variable. 
@app.route('/workout/<workoutID>')
# This route will only run if the user is logged in.
@login_required
def workout(workoutID):
    # retrieve the blog using the blogID
    thisWorkout = Workout.objects.get(id=workoutID)
    # If there are no comments the 'comments' object will have the value 'None'. Comments are 
    # related to blogs meaning that every comment contains a reference to a blog. In this case
    # there is a field on the comment collection called 'blog' that is a reference the Blog
    # document it is related to.  You can use the blogID to get the blog and then you can use
    # the blog object (thisBlog in this case) to get all the comments.
    # Send the blog object and the comments object to the 'blog.html' template.
    return render_template('workout.html',workout=thisWorkout)

# This route will delete a specific blog.  You can only delete the blog if you are the author.
# <blogID> is a variable sent to this route by the user who clicked on the trash can in the 
# template 'blog.html'. 
# TODO add the ability for an administrator to delete blogs. 
@app.route('/workout/delete/<workoutID>')
# Only run this route if the user is logged in.
@login_required
def workoutDelete(workoutID):
    delWorkout = Workout.objects.get(id=workoutID)
    delWorkout.delete()
    return redirect(url_for('workouts'))

# This route actually does two things depending on the state of the if statement 
# 'if form.validate_on_submit()'. When the route is first called, the form has not 
# been submitted yet so the if statement is False and the route renders the form.
# If the user has filled out and succesfully submited the form then the if statement
# is True and this route creates the new blog based on what the user put in the form.
# Because this route includes a form that both gets and blogs data it needs the 'methods'
# in the route decorator.
@app.route('/workout/new', methods=['GET', 'POST'])
# This means the user must be logged in to see this page
@login_required
# This is a function that is run when the user requests this route.
def workoutNew():
    # This gets the form object from the form.py classes that can be displayed on the template.
    form = WorkoutForm()

    # This is a conditional that evaluates to 'True' if the user submitted the form successfully.
    # validate_on_submit() is a method of the form object. 
    if form.validate_on_submit():

        # This stores all the values that the user entered into the new blog form. 
        # Blog() is a mongoengine method for creating a new blog. 'newBlog' is the variable 
        # that stores the object that is the result of the Blog() method.  
        newWorkout = Workout(
            # the left side is the name of the field from the data table
            # the right side is the data the user entered which is held in the form object.
            excercise = form.excercise.data,
            weight = form.weight.data,
            sets = form.sets.data,
            reps = form.reps.data,
            # This sets the modifydate to the current datetime.
        )
        # This is a method that saves the data to the mongoDB database.
        newWorkout.save()

        # Once the new blog is saved, this sends the user to that blog using redirect.
        # and url_for. Redirect is used to redirect a user to different route so that 
        # routes code can be run. In this case the user just created a blog so we want 
        # to send them to that blog. url_for takes as its argument the function name
        # for that route (the part after the def key word). You also need to send any
        # other values that are needed by the route you are redirecting to.
        return redirect(url_for('workout',workoutID=newWorkout.id))

    # if form.validate_on_submit() is false then the user either has not yet filled out
    # the form or the form had an error and the user is sent to a blank form. Form errors are 
    # stored in the form object and are displayed on the form. take a look at blogform.html to 
    # see how that works.
    return render_template('workoutform.html',form=form)


# This route enables a user to edit a blog.  This functions very similar to creating a new 
# blog except you don't give the user a blank form.  You have to present the user with a form
# that includes all the values of the original blog. Read and understand the new blog route 
# before this one. 
@app.route('/workout/edit/<workoutID>', methods=['GET', 'POST'])
@login_required
def workoutEdit(workoutID):
    editWorkout = Workout.objects.get(id=workoutID)
    # if the user that requested to edit this blog is not the author then deny them and
    # send them back to the blog. If True, this will exit the route completely and none
    # of the rest of the route will be run.
    if current_user != editWorkout.author:
        flash("You can't edit a Workout you don't own.")
        return redirect(url_for('workout',workoutID=workoutID))
    # get the form object
    form = WorkoutForm()
    # If the user has submitted the form then update the blog.
    if form.validate_on_submit():
        # update() is mongoengine method for updating an existing document with new data.
        editWorkout.update(
            excercise = form.excercise.data,
            weight = form.weight.data,
            sets = form.sets.data,
            reps = form.reps.data,
        )
        # After updating the document, send the user to the updated blog using a redirect.
        return redirect(url_for('workout',workoutID=workoutID))

    # if the form has NOT been submitted then take the data from the editBlog object
    # and place it in the form object so it will be displayed to the user on the template.
    form.excercise.data = editWorkout.excercise
    form.weight.data = editWorkout.weight
    form.sets.data = editWorkout.sets
    form.reps.data = editWorkout.reps


    # Send the user to the blog form that is now filled out with the current information
    # from the form.
    return render_template('workoutform.html',form=form)