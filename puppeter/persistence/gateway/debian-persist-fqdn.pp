file { '/etc/hostname':
  ensure  => 'file',
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  content => '@{hostname}'
}
