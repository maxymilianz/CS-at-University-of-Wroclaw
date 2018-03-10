import unittest

import prev1
import new1
import exc3


class TestProperDividers(unittest.TestCase):
    non_number_values = ['foo', (), [], {}, set()]
    proper_dividers_values = [(-1, []), (19, [1]), (69, [1, 3, 23]), (13, [1]), (37, [1]), (94, [1, 2, 47]), (21, [1, 3, 7]), (97, [1])]
    proper_dividers_map_values = [(-1, []), (0, [[]]), (1, [[], []]), (2, [[], [], [1]]), (3, [[], [], [1], [1]]), (4, [[], [], [1], [1], [1, 2]])]

    def test_proper_dividers_list(self):
        """Testing proper_dividers_list function"""

        for arg in self.non_number_values:
            self.assertRaises(TypeError, prev1.proper_dividers_list, arg)

        for arg, val in self.proper_dividers_values:
            self.assertEqual(prev1.proper_dividers_list(arg), val)

    def test_proper_dividers_fun(self):
        """Testing proper_dividers_fun function"""

        for arg in self.non_number_values:
            self.assertRaises(TypeError, prev1.proper_dividers_fun, arg)

        for arg, val in self.proper_dividers_values:
            self.assertEqual(prev1.proper_dividers_fun(arg), val)

    def test_proper_dividers_map(self):
        """Testing proper_dividers_map function"""

        for arg in self.non_number_values:
            self.assertRaises(TypeError, prev1.proper_dividers_map, arg)

        for arg, val in self.proper_dividers_map_values:
            self.assertEqual(prev1.proper_dividers_map(arg), val)

    def test_proper_dividers_iter(self):
        """Testing proper_dividers_iter function"""

        for arg in self.non_number_values:
            self.assertRaises(TypeError, lambda n: list(new1.proper_dividers_iter(n)), arg)

        for arg, val in self.proper_dividers_values:
            self.assertEqual(list(new1.proper_dividers_iter(arg)), val)


class TestPrimes(unittest.TestCase):
    non_number_values = ['foo', (), [], {}, set()]
    primes_values = [(-1, []), (19, [2, 3, 5, 7, 11, 13, 17, 19]), (69, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67]),
                     (13, [2, 3, 5, 7, 11, 13]), (37, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]),
                     (94, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89]),
                     (21, [2, 3, 5, 7, 11, 13, 17, 19]),
                     (97, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97])]

    def test_primes_list(self):
        """Testing primes_list function"""

        for arg in self.non_number_values:
            self.assertRaises(TypeError, prev1.primes_list, arg)

        for arg, val in self.primes_values:
            self.assertEqual(prev1.primes_list(arg), val)

    def test_primes_fun(self):
        """Testing primes_fun function"""

        for arg in self.non_number_values:
            self.assertRaises(TypeError, prev1.primes_fun, arg)

        for arg, val in self.primes_values:
            self.assertEqual(prev1.primes_fun(arg), val)

    def test_primes_map(self):
        """Testing primes_map function"""

        for arg in self.non_number_values:
            self.assertRaises(TypeError, prev1.primes_map, arg)

        for arg, val in self.primes_values:
            self.assertEqual(prev1.primes_map(arg), val)

    def test_primes_iter(self):
        """Testing primes_iter function"""

        for arg in self.non_number_values:
            self.assertRaises(TypeError, lambda n: list(new1.primes_iter(n)), arg)

        for arg, val in self.primes_values:
            self.assertEqual(list(new1.primes_iter(arg)), val)


class TestPerfectNumbers(unittest.TestCase):
    non_number_values = ['foo', (), [], {}, set()]
    perfect_numbers_values = [(-1, []), (19, [0, 6]), (69, [0, 6, 28]), (13, [0, 6]), (37, [0, 6, 28]), (94, [0, 6, 28]), (21, [0, 6]), (97, [0, 6, 28])]
    perfect_numbers_iter_values = [(-1, []), (19, [6]), (69, [6, 28]), (13, [6]), (37, [6, 28]), (94, [6, 28]), (21, [6]), (97, [6, 28])]

    def test_perfect_numbers_list(self):
        """Testing perfect_numbers_list function"""

        for arg in self.non_number_values:
            self.assertRaises(TypeError, prev1.perfect_numbers_list, arg)

        for arg, val in self.perfect_numbers_values:
            self.assertEqual(prev1.perfect_numbers_list(arg), val)

    def test_perfect_numbers_fun(self):
        """Testing perfect_numbers_fun function"""

        for arg in self.non_number_values:
            self.assertRaises(TypeError, prev1.perfect_numbers_fun, arg)

        for arg, val in self.perfect_numbers_values:
            self.assertEqual(prev1.perfect_numbers_fun(arg), val)

    def test_perfect_numbers_iter(self):
        """Testing perfect_numbers_iter function"""

        for arg in self.non_number_values:
            self.assertRaises(TypeError, lambda n: list(new1.perfect_numbers_iter(n)), arg)

        for arg, val in self.perfect_numbers_iter_values:
            self.assertEqual(list(new1.perfect_numbers_iter(arg)), val)


class TestSentences(unittest.TestCase):
    # I think there's no sense iterating over a set or a dict, as they may have undefined order
    iteration_values = [("We all do dumb things, that's what makes us humans.",
                         ["We all do dumb things, that's what makes us humans."]), (
                            "A great beast is walking through the sands, and they are climbing into the air, and now they are making a tear, and now they are gone, and now you are here. Little creatures are walking through the air, and they are dragging in places and echoes of lives, and they are asking me about God. I am going to tell you something, little creature. You are swimming further and further out to sea, and beyond are things blind and terrible, and I am showing you now. They are blind, but they are seeing you. And you are coming to them. After this, you are not returning here. I am climbing into the air and closing the sky.",
                            [
                                "A great beast is walking through the sands, and they are climbing into the air, and now they are making a tear, and now they are gone, and now you are here.",
                                " Little creatures are walking through the air, and they are dragging in places and echoes of lives, and they are asking me about God.",
                                " I am going to tell you something, little creature.",
                                " You are swimming further and further out to sea, and beyond are things blind and terrible, and I am showing you now.",
                                " They are blind, but they are seeing you.", " And you are coming to them.",
                                " After this, you are not returning here.",
                                " I am climbing into the air and closing the sky."]),
                        (['s', 'h', 'o', 'r', 't', '.'], ['short.']),
                        (('2', '.', 's', 'h', 'o', 'r', 't', '.'), ['2.', 'short.'])]
    bad_iteration_values = [([
                                 "War is where the young and stupid are tricked by the old and bitter into killing each other."],
                             [
                                 "War is where the young and stupid are tricked by the old and bitter into killing each other."])]

    corrected_values = [('lower case.', 'Lower case.'), ('No dot', 'No dot.'), ('Whitespace. ', 'Whitespace.'),
                        ('all three ', 'All three.')]

    def test_iterating(self):
        """Testing iterating over a Sentences object"""

        self.assertRaises(TypeError, lambda n: list(iter(exc3.Sentences(n))), 161)

        for arg, val in self.iteration_values:
            self.assertEqual(list(iter(exc3.Sentences(arg))), val)

        for arg, val in self.bad_iteration_values:
            self.assertNotEqual(list(iter(exc3.Sentences(arg))), val)

    def test_correct(self):
        """Testing Sentences.correct function"""

        self.assertRaises(TypeError, exc3.Sentences.correct, 161)
        self.assertRaises(IndexError, exc3.Sentences.correct, [])
        self.assertRaises(IndexError, exc3.Sentences.correct, ())
        self.assertRaises(KeyError, exc3.Sentences.correct, {})
        self.assertRaises(TypeError, exc3.Sentences.correct, set())

        for arg, val in self.corrected_values:
            self.assertEqual(exc3.Sentences.correct(arg), val)


unittest.main()