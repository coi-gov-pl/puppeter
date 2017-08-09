augeas { 'persist-hostname':
  context => '/files/etc/sysconfig/network',
  changes => 'set HOSTNAME @{hostname}'
}
