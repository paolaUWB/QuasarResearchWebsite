User Management 
===============

1. The user database and login system follows these
two tutorials
    1. https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database    
    1. https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
        

1. To view all users 1. ``flask shell``
   1. See list of all usernames
       1. `users = User.query.all()`
       1. `users`

   1. See list of ids of users
       1. `users = User.query.all()`
       1.
        ::
            for u in users:
              ...     print(u.id, u.username)
              ...

2. To add a user
    1. `flask shell`
    1. `u = User(username='INSERT USERNAME HERE', email='INSERT EMAIL HERE')`
    1. `u.set_password('INSERT PASSWORD HERE')`
    1. `db.session.add(u)`
    1. `db.session.commit()`

3. To delete all users
    1. `flask shell`

    1. `users = User.query.all()`

    1.
        ::
          for u in users:
          ...     db.session.delete(u)
          ...

    1. `db.session.commit()`

   1. To delete a specific user

      1. ``flask shell``

      2. Find the id of the user you want to delete.

      3. ``u = User.query.get(INSERT ID HERE)``

      4. ``db.session.delete(u)``

      5. ``db.session.commit()``
