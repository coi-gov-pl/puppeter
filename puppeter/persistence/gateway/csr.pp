file { "${settings::confdir}/csr_attributes.yaml":
  ensure  => 'file',
  owner   => 'puppet',
  group   => 'puppet',
  mode    => '0640',
  content => '@{content}'
}
