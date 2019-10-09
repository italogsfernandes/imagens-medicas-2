from django_hosts import patterns, host

host_patterns = patterns(
    'path.to',
    host(r'imagens-medicas-2', 'im2webapp.urls', name='im2webapp'),
)
