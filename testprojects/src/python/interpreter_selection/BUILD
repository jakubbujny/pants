# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).


# Note that targets in this BUILD file have deliberately conflicting interpreter specifications.

python_library(
  name = 'echo_interpreter_version_lib',
  sources = ['echo_interpreter_version.py'],
  dependencies = [],
  # Play with this to test interpreter selection in the pex machinery.
  # TODO(John Sirois): Allow `<4` when the issues with `3.7` are fixed. See:
  #   https://github.com/pantsbuild/pants/issues/6363
  compatibility = ['CPython>=2.7,<3.7']
)

python_binary(
  name = 'echo_interpreter_version_3',
  dependencies = [
    ':echo_interpreter_version_lib',
  ],
  entry_point = 'interpreter_selection.echo_interpreter_version',
  compatibility = ['CPython>=3.3']
)

python_binary(
  name = 'echo_interpreter_version_2.7',
  dependencies = [
    ':echo_interpreter_version_lib',
  ],
  entry_point = 'interpreter_selection.echo_interpreter_version',
  compatibility = ['CPython>=2.7,<3']
)

# Note: Used by tests, but also useful for manual testing.
python_binary(
  name = 'echo_interpreter_version',
  dependencies = [
    ':echo_interpreter_version_lib',
  ],
  entry_point = 'interpreter_selection.echo_interpreter_version',
)

# Note: Used by tests, but also useful for manual testing.
python_binary(
  name = 'deliberately_conficting_compatibility',
  dependencies = [
    ':echo_interpreter_version_lib',
  ],
  entry_point = 'interpreter_selection.echo_interpreter_version',
  compatibility = ['CPython<2.7']
)

python_library(
  name = 'die_lib',
  sources = ['die.py'],
  dependencies = [],
  compatibility = ['CPython>=2.7,<3']
)

python_binary(
  name = 'die',
  dependencies = [
    ':die_lib',
  ],
  entry_point = 'interpreter_selection.die',
)
