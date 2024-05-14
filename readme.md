from market.models import db
>>> from market import app
>>> app.app_context().push()
>>> db.drop_all()
> u1 = User(username='Aryant', password_hash = '123456', email='ary@gmail.com')
> 
from market.models import Item,User, db
from market import app
app.app_context().push()
u1 = User(username='Aryant', password_hash = '123456', email='ary@gmail.com')
db.session.close_all()
db.session.add(u1)
db.session.commit()
i1 = Item(name='Iphone15', description='description', barcode='123456789023',price'799')

**Q.** but i cant see any column named owned_user in item table
**A.** You're correct. There isn't a physical column named owned_user in the Item table. Instead, the backref argument
in the relationship definition sets up a way to navigate the relationship in Python code. It creates a virtual 
attribute called owned_user on instances of the Item class, which allows you to access the related User object.

So, when you access item.owned_user, SQLAlchemy internally performs a query to find the user associated with that item 
based on the foreign key relationship specified by owner.

Think of it like a shortcut or alias for accessing related objects. It's not stored in the database; it's created 
on-the-fly when needed. This is a convenience provided by SQLAlchemy to simplify working with relationships between
tables.

**Q** that means this column does not exists it only helps to fetch the related records 

**A.** Exactly. The backref argument in SQLAlchemy is a tool for setting up relationships between models in a way 
that makes it easier to navigate those relationships in your Python code. It doesn't create an actual column 
in the table. Instead, it sets up a way to access related records conveniently. When you access the backref 
attribute, SQLAlchemy handles the necessary database queries to retrieve the related records based on the 
defined relationship.

**Q.** one more thing why there is no items column in user table
**A.** In SQLAlchemy, when you establish a one-to-many relationship between two tables using the relationship function,
it doesn't create an actual column in the table. Instead, SQLAlchemy handles this relationship at the ORM
(Object-Relational Mapping) level.

_items = db.relationship('Item', backref='owned_user', lazy=True)_
his line indicates that a User can have multiple Item instances associated with it. However, there's no need to create
an items column in the User table to represent this relationship. Instead, SQLAlchemy manages this relationship
internally.

When you access user.items, SQLAlchemy will automatically query the Item table to find all items associated with the 
given user by looking at the foreign key relationship established in the Item table.

So, in summary, in SQLAlchemy, relationships between tables are managed at the ORM level, and there's no need to 
represent these relationships as actual columns in the tables themselves.
