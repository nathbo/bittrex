import time
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def loop(func):
    """Loop decorator - Useful if stability is 100% necessary

    Sometimes API queries get weird bugs, so this decorator catches
    every exception and just tries again.

    Defines `n_tries` and `sleep`, but gets overridden if called on
    a class function and the corresponding `self` has those attributes.

    Parameters
    ----------
    func : function
        Function to decorate
    n_tries : int
        Number of tries (default=100)
    sleep : int
        Seconds to sleep between loops (default=10)

    Returns
    -------
    function
        Looped function
    """
    n_tries = 100
    sleep = 10

    def looped_func(*args, **kwargs):
        self = args[0]
        if hasattr(self, 'n_tries'):
            n_tries = self.n_tries
        if hasattr(self, 'sleep'):
            sleep = self.sleep
        for i in range(n_tries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f'Try {i+1} failed with Error {e}')
                time.sleep(sleep)
    return looped_func
