Introduction
============

This is a full-blown functional test. The emphasis here is on testing what
the user may input and see, and the system is largely tested as a black box.
We use PloneTestCase to set up this test as well, so we have a full Plone site
to play with. We *can* inspect the state of the portal, e.g. using 
self.portal and self.folder, but it is often frowned upon since you are not
treating the system as a black box. Also, if you, for example, log in or set
roles using calls like self.setRoles(), these are not reflected in the test
browser, which runs as a separate session.

Being a doctest, we can tell a story here.

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the 
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

Because add-on themes or products may remove or hide the login portlet, this test will use the login form that comes with plone.  

    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.  We then ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True

Finally, let's return to the front page of our site before continuing

    >>> browser.open(portal_url)

-*- extra stuff goes here -*-
The Downloadablefile content type
===============================

In this section we are tesing the Downloadablefile content type by performing
basic operations like adding, updadating and deleting Downloadablefile content
items.

Adding a new Downloadablefile content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Downloadablefile' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Downloadablefile').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Downloadablefile' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Downloadablefile Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Downloadablefile' content item to the portal.

Updating an existing Downloadablefile content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Downloadablefile Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Downloadablefile Sample' in browser.contents
    True

Removing a/an Downloadablefile content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Downloadablefile
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Downloadablefile Sample' in browser.contents
    True

Now we are going to delete the 'New Downloadablefile Sample' object. First we
go to the contents tab and select the 'New Downloadablefile Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Downloadablefile Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Downloadablefile
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Downloadablefile Sample' in browser.contents
    False

Adding a new Downloadablefile content item as contributor
------------------------------------------------

Not only site managers are allowed to add Downloadablefile content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Downloadablefile' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Downloadablefile').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Downloadablefile' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Downloadablefile Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Downloadablefile content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The templateproject content type
===============================

In this section we are tesing the templateproject content type by performing
basic operations like adding, updadating and deleting templateproject content
items.

Adding a new templateproject content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'templateproject' and click the 'Add' button to get to the add form.

    >>> browser.getControl('templateproject').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'templateproject' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'templateproject Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'templateproject' content item to the portal.

Updating an existing templateproject content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New templateproject Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New templateproject Sample' in browser.contents
    True

Removing a/an templateproject content item
--------------------------------

If we go to the home page, we can see a tab with the 'New templateproject
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New templateproject Sample' in browser.contents
    True

Now we are going to delete the 'New templateproject Sample' object. First we
go to the contents tab and select the 'New templateproject Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New templateproject Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New templateproject
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New templateproject Sample' in browser.contents
    False

Adding a new templateproject content item as contributor
------------------------------------------------

Not only site managers are allowed to add templateproject content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'templateproject' and click the 'Add' button to get to the add form.

    >>> browser.getControl('templateproject').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'templateproject' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'templateproject Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new templateproject content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The TemplateUploadCenter content type
===============================

In this section we are tesing the TemplateUploadCenter content type by performing
basic operations like adding, updadating and deleting TemplateUploadCenter content
items.

Adding a new TemplateUploadCenter content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'TemplateUploadCenter' and click the 'Add' button to get to the add form.

    >>> browser.getControl('TemplateUploadCenter').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'TemplateUploadCenter' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'TemplateUploadCenter Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'TemplateUploadCenter' content item to the portal.

Updating an existing TemplateUploadCenter content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New TemplateUploadCenter Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New TemplateUploadCenter Sample' in browser.contents
    True

Removing a/an TemplateUploadCenter content item
--------------------------------

If we go to the home page, we can see a tab with the 'New TemplateUploadCenter
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New TemplateUploadCenter Sample' in browser.contents
    True

Now we are going to delete the 'New TemplateUploadCenter Sample' object. First we
go to the contents tab and select the 'New TemplateUploadCenter Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New TemplateUploadCenter Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New TemplateUploadCenter
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New TemplateUploadCenter Sample' in browser.contents
    False

Adding a new TemplateUploadCenter content item as contributor
------------------------------------------------

Not only site managers are allowed to add TemplateUploadCenter content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'TemplateUploadCenter' and click the 'Add' button to get to the add form.

    >>> browser.getControl('TemplateUploadCenter').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'TemplateUploadCenter' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'TemplateUploadCenter Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new TemplateUploadCenter content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)



