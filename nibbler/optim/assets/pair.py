from . import Feed


def check_feed_and_wait_(self, feeds, wait):

    assert len(feeds) == len(wait), "feeds must be same length as wait"

    if len(feeds) > 1:

        for feed in feeds:
            assert isinstance(feed, Feed), "input must be a list of feeds"
        
        feed_len = len(feeds)

        for feed in feeds:
            assert len(feed)==feed_len, "all feeds must be of the same length"

        for w in wait:
            assert isinstance(w, int), "wait specified must be integers" 
    else:

        assert wait[0] == 1, "with only a single feed there should be not wait"
    

class Pair:

    __slots__ = [
        "feed_dict", "name", "iter_dict", "n",
        "feed_len"
    ]

    def __init__(self, feeds, wait, name=None):

        self.feed_len = len(feeds[0])

        check_feed_and_wait_(self, feeds, wait)
        
        self.name = name

        self.feed_dict = dict(
            [
                (w, feed) for w, feed in zip(wait, feeds)
            ]
        )
    
    def __len__(self):
        return self.feed_len

    def __iter__(self):
        self.iter_dict = dict(
            (w, iter(feed)) for w, feed in self.feed_dict.values()
        ) 
        self.n = 0
        return self
     
    def __next__(self):

        if self.n > self.feed_dict:
            raise StopIteration

        self.n += 1

        return dict(
            (w, next(feed)) for w, feed in self.iter_dict
        )
