[![Build Status](https://travis-ci.org/tdpsk/flask-miracle-acl.svg?branch=master)](https://travis-ci.org/tdpsk/flask-miracle-acl)

# Introduction

This library provides a small fabric code layer which connects the
[Miracle ACL](https://github.com/kolypto/py-miracle) library for Python to the
well-known and widely used [Flask](http://flask.pocoo.org/) framework.

# Configuration

In order to actively use the library connector, it needs to be configured.
Configuration is done via the Flask configuration environment, whereby the
following configuration options are currently supported:

* `MACL_DEFINITION`: the ACL definition in one Python dict object. The dict can
  have three fields:
  * `struct`: structure to be used in the format of the Miracle [add(structure)](https://github.com/kolypto/py-miracle#addstructure)
    method
  * `roles`: a list of roles as string identifiers
  * `grants`: a Python dict object defining the grants as described in the Miracle [grants(...)](https://github.com/kolypto/py-miracle#grantsgrants) method
* `MACL_CLASS`: A class describing the roles, structure and grants which should
  be loaded. The required class parameters are STRUCT, ROLES and GRANTSAcl(app), which
  follow the same format described within `MACL_DEFINITION`
* `MACL_ERROR_MESSAGE`: The error message that will be used as the description
  within the exception raised if insufficient privileges are discovered

# Initializing

Initializing flask-miracle-acl is as easy as passing it the Flask app you wish to use it with:

```Python
from flask_miracle import Acl
macl = Acl(app)
```

The constructor of the Acl class takes two arguments

```Python
def __init__(self, app=None, acl=None):
  ...
```

where app is a Flask app instance and acl is an existing Miracle ACL instance. Please note both arguments are optional at initialization and can be set / changed at runtime.

# Setting access roles

In order to be able to use flask-miracle-acl to determine if a user has sufficient privileges to access a Flask resource, the currently active roles need to be made available to the system. There are two ways to set the current roles:

## Using set_current_roles

Calling the `set_current_roles` method with a list of role names as parameter will set the current roles within the Acl class.

## Using set_roles_callback

The method `set_roles_callback` can be used to create a more versatile environment by passing a function as parameter to the function. When an authorization request is handled, the callback function will always be called to determine the currently valid roles - this allows for changing roles during the request.

Note: if a callback function is set, any roles previously set using `set_current_roles` will be ignored.

# Determining access privileges

During the course of a request handled by the Flask app, you may want to check whether the user has sufficient privileges to access the resource requested. There are two ways to implement this:

## Using methods

The miracle_acl package has two methods which allow you to verify the access privileges of a role.

The methods are also available as methods of the Acl class for use outside the Flask request context.

* `check_all`: Returns True if all currently active roles have access to the requested resource, False otherwise

* `check_any`: Return True if any of the currently active roles has access to the requested resource, False otherwise

Both methods take the same three arguments:

* `resource`: The resource to check access privileges on
* `permission`: The permission within the defined resource to check access privileges on
* `roles`: defaults to None. If set to a list of roles, this will override any other definition of currently active roles. Note: the role callback function will not be called in this case

## Using decorators

For each of the two methods, a corresponding decorator is available which allows you to check access to a Flask app resource prior to executing the contained code. The decorators are called `macl_check_any` and `macl_check_all` respectively.

Both decorators take the corresponding resource and permission as parameters.
