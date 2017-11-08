augeas { 'puppet.conf':
  context => "/files${settings::confdir}/puppet.conf",
  changes => [
    @{settings}
  ],
}
