import signal
import unittest
from task2_task6 import evklid_nod


def timeout(nsec, error_message="Execution timeout"):
    def _timeout_handler(signum, frame):
        raise TimeoutError(f"{error_message}: {nsec}")

    def wrapper(func):
        def _wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _timeout_handler)
            signal.setitimer(signal.ITIMER_REAL, nsec)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return _wrapper
    return wrapper


class Task6Test(unittest.TestCase):
    @timeout(0.1)
    def test_evklid_nod1(self):
        self.assertEqual(evklid_nod(1000, 100), 100)

    @timeout(0.1)
    def test_evklid_nod2(self):
        self.assertEqual(evklid_nod(1000, 55), 5)

    @timeout(0.1)
    def test_evklid_nod3(self):
        self.assertEqual(evklid_nod(111, 35), 1)

    @timeout(0.1)
    def test_evklid_nod4(self):
        self.assertEqual(evklid_nod(111, -78), -3)

    @timeout(0.1)
    def test_evklid_nod5(self):
        self.assertEqual(evklid_nod(-9876, -78), -6)


if __name__ == '__main__':
    unittest.main()
