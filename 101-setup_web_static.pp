# Ensure the web_static directory exists
file { '/data/web_static':
  ensure => 'directory',
}

# Create a symbolic link to the releases/test directory
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  require => File['/data/web_static'],
}

# Create the releases/test directory
file { '/data/web_static/releases/test':
  ensure => 'directory',
}

# Create an index.html file inside releases/test directory
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '<html>\n<head>\n</head>\n<body>\nHolberton School\n</body>\n</html>\n',
  require => File['/data/web_static/releases/test'],
}
