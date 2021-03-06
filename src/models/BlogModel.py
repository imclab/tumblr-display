import PostModel

class BlogModel(object):

    def __init__(self, client, account):
        self.client = client
        self.sAccount = account

        blog_info = client.posts(self.sAccount)

        self.sName = blog_info['blog']['title']
        self.nNumPosts = blog_info['total_posts']

        self.loaded = set()

        print "Created model for blog " + self.getName()

    def getName(self):
        return self.sName

    def getNumPosts(self):
        return self.nNumPosts

    def getPosts(self, start=0, end=19, types=['photo', 'video']):
        n = 0
        N = (end + 1) - start

        print str(start) + ", " + str(end)

        posts = []
        i = 0
        while n < N:
            grab = min(N - n, 20)
            ps = self.client.posts(self.sAccount, limit=grab, offset= (start + i))

            for p in ps['posts']:
                if p['type'] in types:
                    if p['id'] in self.loaded:
                        print "DUPE! " + str(p['id'])
                    self.loaded.add(p['id'])
                    print 'post of type ' + p['type'] + '\tid: ' + str(p['id'])
                    posts.append(PostModel.MakePostModel(p))
                    n += 1
                i += 1

        print 'retrieved ' + str(len(posts))
        return posts, start + i