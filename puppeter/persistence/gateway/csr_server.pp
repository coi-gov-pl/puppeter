file { "${settings::confdir}/csr_attributes.yaml":
  ensure  => 'file',
  mode    => '0640',
  group   => 'puppet',
  content => '@{content}',
}
