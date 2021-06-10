from cwutils.SocialMedia import get_sharing_url
import validators

def is_url(string):
    return validators.url(string)


def url_domain(url):
    protocol, domain = url.split('//')
    parts = domain.split('?')
    domain = parts[0]
    return domain.split('/')[0]


def url_from_base(base, an_id, *additional):
    raw = '%s/%s' % (base, an_id)
    if additional:
        return '%s/%s' % (raw, '/'.join(additional))
    return raw


def twitter_share_url(url, text='', *tags):
    return get_sharing_url('twitter', url=url, title=text, hash_tags=' '.join(tags))


def linkedin_share_url(url):
    return get_sharing_url('linkedin', url=url)


def facebook_share_url(url):
    return get_sharing_url('facebook', url=url)


def get_url(type, ids=None):
    if type == 'content':
        return '/content/%s' % ids['content_id']
    elif type == 'comment':
        return '/content/%s#comment_id=%s' % (ids['content_id'], ids['comment_id'])
    elif type == 'user':
        return '/profile/%s' % ids['user_id']
    elif type == 'group':
        return '/group/%s' % ids['group_id']
