$cfgdir = $::osfamily ? {
  'Debian' => '/etc/default',
  'RedHat' => '/etc/sysconfig',
  default  => fail("Unsupported OS Family: ${::osfamily}")
}
augeas { 'settings-of-puppetserver':
  context => "/files${cfgdir}/puppetserver",
  changes => [
    "set JAVA_ARGS '\"@{jvmargs}\"'"
  ],
}
