from . import Feed
import re


timeframe_suffixes_ = ["m", "h", "d", "w", "M"]
timeframe_suffix_dict_ = dict(
    m=1,
    h=60,
    d=60*24,
    M=60*24*30,
)


class Pair:

    __slots__ = [
        "feed_list", "name", "delay",
        "max_len", "iter_list", "nskip",
        "n", "wait", "counter", "start_time"
    ] 

    def __init__(self, name: str):

        self.feed_list = []
        self.name = name
        self.delay = 0
        self.max_len = 0
        self.nskip = 0
        self.wait = 0

    def __len__(self):

        return self.max_len

    def add_feed(self, feed:Feed):

        assert feed.timeframe is not None, \
            "feed timeframe must not be none"

        multiplier = re.findall("[0-9]+", feed.timeframe)[0]
        multiplier = int(multiplier)

        timeframe_string = re.findall("[a-z]+", feed.timeframe)[0]
        timeframe = timeframe_suffix_dict_[timeframe_string]

        self.feed_list.append(
            (multiplier*timeframe, feed)
        )
        
        self.feed_list.sort(key=lambda x: x[0])
        # set the wait times based off the case with the lowest time scale
        if len(self.feed_list) > 0:
            minutes = self.feed_list[0][0]

            for item in self.feed_list:
                wait_multiplier = item[0]/minutes
                item[-1].wait = int(wait_multiplier)
        # find the maximum length of all the datasets
        self.max_len = 10000000000
        for (_, feed) in self.feed_list:
            if len(feed) < self.max_len:
                self.max_len = len(feed)
        # set the maximul length of all the datasets
        for (_, feed) in self.feed_list:
            feed.max_len = self.max_len
        # set the nkip of all the sets
        self.nskip = self.feed_list[0][-1].nskip 
        for (_, feed) in self.feed_list:
            feed.nskip = self.nskip/feed.wait
        # calculate the start time based off of the datafeeds
        start_time = 1000000000
        for _, feed in self.feed_list:
            start = feed.data[0][0]
            if start < start_time:
                self.start_time = start

    def __iter__(self):

        self.n = self.nskip

        self.counter = 0

        self.iter_list = [
            (feed.timeframe, iter(feed)) for
            timeframe, feed in self.feed_list
        ]

        return self

    def __next__(self):

        self.counter += 1

        if self.counter > self.wait:

            if self.n > self.max_len:
                raise StopIteration
            
            return dict(
                [
                    (timeframe, next(feed)) for
                    timeframe, feed in self.iter_list
                ]
            )
        return None