# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import redirect, render_template, render_template_string, Blueprint
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted
from app.init_app import app, db
from app.models import UserProfileForm
# from app.models import UserCodeForm
from app.models import CheckForm
from app.models import Codes_T
from wtforms import ValidationError

# The Home page is accessible to anyone
@app.route('/')
def home_page():
    return render_template('pages/home_page.html')

@app.route('/success')
def success():
    return render_template('pages/success.html')

@app.route('/try_again')
def try_again():
    return render_template('pages/wrong.html')

# The User page is accessible to authenticated users (users that have logged in)
@app.route('/user' , methods=['GET', 'POST'])
@login_required  # Limits access to authenticated users
def user_page():
    form = CheckForm()
    data = ''
    code = form.some_code.data
    if request.method == 'POST':
        check_code = Codes_T.query.filter_by(codenumber=code).first()
        if check_code:
            # data = 'CONGRATULATIONS ! U HAVE DONE IT'
            return  redirect(url_for('success'))
            # return redirect(url_for('home_page'))
        else:
            # data = 'WRONG CODE PLEASE TRY AGAIN'
            return redirect(url_for('try_again'))

    # form = UserCodeForm(request.form)
    #
    # if request.method == 'POST':
    #     code = request.form['code']
    #     print code
    #     if code.data != Codes.code:
    #         raise ValidationError('Wrong Code! Please Try Again.')
    return render_template('pages/user_page.html', form=form, data=data)


# The Admin page is accessible to users with the 'admin' role
@app.route('/admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('pages/admin_page.html')


@app.route('/pages/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('home_page'))

    # Process GET or invalid POST
    return render_template('pages/user_profile_page.html',
                           form=form)
