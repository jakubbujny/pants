Developing a Pants Plugin
=========================

This page documents how to develop a Pants plugin, a set of code that
defines new Pants functionality. If you
[[develop a new task|pants('src/docs:dev_tasks')]]
or target to add to Pants (or to
override an existing part of Pants), a plugin gives you a way to
register your code with Pants.

Much of Pants' own functionality is organized in plugins; see them in
[`src/python/pants/backend/*`](https://github.com/pantsbuild/pants/tree/master/src/python/pants/backend).

A plugin registers its functionality with Pants by defining some
functions in a `register.py` file in its top directory. For example,
Pants' `jvm` code registers in
[src/python/pants/backend/jvm/register.py](https://github.com/pantsbuild/pants/blob/master/src/python/pants/backend/jvm/register.py)
Pants' backend-loader code assumes your plugin has a `register.py` file
there.

Hello world plugin with its own goal
--------------------

The hello world plugin shows how to register your plugin to Pants and define its own `hello-world` goal which contains 2 tasks and 
which can be executed by Pants. To achieve that, take a look at the following steps:
- Create a new Pants project so you have pants.ini file in root of your repository

- Create a home directory for your plugins. In this example we will use `plugins/` directory in root of repository,
but the word "plugins" is not special for Pants.

- In the `plugins/` directory, create following filesystem structure:

      hello/
        __init__.py
        register.py
        tasks/
           __init__.py
           your_tasks.py
        
        
- `__init__.py` files can be empty - you're just saying to Python that you created modules.

- In `your_tasks.py` place the following content:

      from pants.task.task import Task
          
      class HelloTask(Task):
          def execute(self):
              print("Hello")
     
      class WorldTask(Task):
          def execute(self):
              print("world!")
   [Task](https://github.com/pantsbuild/pants/blob/master/src/python/pants/task/task.py) is a simple base
   class for your tasks - you need to implement an `execute` method which will be executed by Pants.
   
- In `register.py` place the following content:

      from pants.goal.goal import Goal
      from pants.goal.task_registrar import TaskRegistrar as task
      from hello.tasks.your_tasks import HelloTask, WorldTask
      
      def register_goals():
          Goal.register(name="hello-world", description="Say hello to your world")
          task(name='hello', action=HelloTask).install('hello-world')
          task(name='world', action=WorldTask).install('hello-world')
          
     Here you register new Pants goal named `hello-world` and documented with a description,
     and then attach 2 tasks to the goal created in previous step.

- In `pants.ini` place the following content:
      
      [GLOBAL]
      pants_version: 1.9.0
      pythonpath: ["%(buildroot)s/plugins"]
      backend_packages: ["hello"]
      
     You need to put your plugins on the `pythonpath` so Pants will know where to find them.
     `backend_packages` defines which plugins you want to use in your project.
     
- You are ready to use your plugin with the `hello-world` goal! First try to find your goal by typing `./pants goals`:

      ...
      hello-world: Say hello to your world
      ...
- Now you can use your plugin by typing `./pants hello-world`:

      ...
      Executing tasks in goals: hello-world
      XX:XX:XX 00:00   [hello-world]
      XX:XX:XX 00:00     [hello]Hello
      
      XX:XX:XX 00:00     [world]world!
      
      XX:XX:XX 00:00   [complete]
                     SUCCESS

Simple Configuration
--------------------

If you want to extend Pants without adding any 3rd-party libraries that aren't already referenced by
Pants, you can use the following technique using sources stored directly in your repo.
All you need to do is name the package where the plugin is defined, and the pythonpath entry to
load it from.

In the example below, the stock `JvmBinary` target is subclassed so that a custom task (not shown)
can consume it specifically but disregard regular `JvmBinary` instances (using `isinstance()`).

- Define a home for your plugins. In this example we'll use a top-level `plugins/` directory but
  this is not special.

- Create an empty `plugins/hadoop/targets/__init__.py` to define a python package structure
  for your custom hadoop target type plugin. Also create empty `__init__.py` files in each
  directory up to but not including the root directory of your python package layout; in this case,
  just `plugins/hadoop/__init__.py`.

- Create a python module for your custom target type in `plugins/hadoop/targets/hadoop_binary.py`:

        :::python
        # plugins/hadoop/targets/hadoop_binary.py
        from pants.backend.jvm.targets.jvm_binary import JvmBinary


        class HadoopBinary(JvmBinary):
          pass


- Create `plugins/hadoop/register.py` to register the elements exposed by your plugin to BUILD file
  authors:

        :::python
        # plugins/hadoop/register.py

        from pants.build_graph.build_file_aliases import BuildFileAliases
        from hadoop.targets.hadoop_binary import HadoopBinary

        def build_file_aliases():
          return BuildFileAliases(
            targets={
              # NB: This allows a HadoopBinary target to be created in a BUILD file using the
              # hadoop_binary alias.
              'hadoop_binary': HadoopBinary,
            },
          )


- In `pants.ini`, add your new plugin package to the list of backends to load when pants starts.
  This instructs pants to load a module named `hadoop.register`.

        :::ini
        [GLOBAL]
        pythonpath: [
            '%(buildroot)s/plugins',
          ]
        backend_packages: [
            'hadoop',
          ]

Note that you can also set the PYTHONPATH in your `./pants` wrapper script, instead of in
`pants.ini`, if you have other reasons to do so. Either way, pants will look for a `register.py`
file for each backend package you list by prefixing that package with the python path; ie roughly
`pythonpath + backend package + register.py` is tried for each pythonpath prefix until a
`register.py` is found, in this example `plugins/hadoop/register.py`.

Examples from `twitter/commons`
-------------------------------

For an example of a code repo with plugins to add features to Pants when building in that repo,
take a look at [`twitter/commons`](https://github.com/twitter/commons), especially its
[`pants-plugins` directory](https://github.com/twitter/commons/tree/32011ab5351fea23e8c70e24e752540b06d1389f/pants-plugins).

The repo's [`pants.ini` file](https://github.com/twitter/commons/blob/32011ab5351fea23e8c70e24e752540b06d1389f/pants.ini) has a
`backend_packages` entry listing the plugin packages (packages with `register.py` files):

    :::ini
    [GLOBAL]
    pythonpath: [
        "%(buildroot)s/pants-plugins/src/python",
      ]
    backend_packages: [
        'twitter.common.pants.jvm.extras',
        'twitter.common.pants.python.commons',
        'pants.contrib.python.checks',
      ]

The [`...jvm/extras/register.py`](https://github.com/twitter/commons/blob/master/pants-plugins/src/python/twitter/common/pants/jvm/extras/register.py)
file registers a `checkstyle` goal. To find the code for this task, come back to the
`pantsbuild/pants` repo: Pants defines the
[`Checkstyle` task class](https://github.com/pantsbuild/pants/blob/master/src/python/pants/backend/jvm/tasks/checkstyle.py) but doesn't register it. 
But other Pants workspaces can register it, as `twitter/commons` illustrates.
