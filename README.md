# pushover-twitter-mentions

This script uses [Pushover][1] to notify the user of mentions of his username on Twitter.

## Setup

I did only test this with Python 2.7.6. It might work with other 2.x versions. It might break.

Use `pip` to install the required PyPI packages

```
$ pip install -r requirements.txt
```

Then edit `push.py` and replace `your_user_key_here` with your Pushover User Key you can find on [the Pushover homepage][1] when logged in, then run the script.

```
$ python push.py
```

[1]: https://pushover.net
