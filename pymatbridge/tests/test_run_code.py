import pymatbridge as pymat
from pymatbridge.compat import text_type
import numpy as np
import numpy.testing as npt
import test_utils as tu


class TestRunCode:

    # Start a Matlab session before running any tests
    @classmethod
    def setup_class(cls):
        cls.mlab = tu.connect_to_matlab()

    # Tear down the Matlab session after running all the tests
    @classmethod
    def teardown_class(cls):
        tu.stop_matlab(cls.mlab)

    # Running 'disp()' in Matlab command window
    def test_disp(self):
        result1 = self.mlab.run_code("disp('Hello world')")['content']['stdout']
        result2 = self.mlab.run_code("disp('   ')")['content']['stdout']
        result3 = self.mlab.run_code("disp('')")['content']['stdout']

        npt.assert_equal(result1, "Hello world\n")
        npt.assert_equal(result2, "   \n")
        if tu.on_octave():
            npt.assert_equal(result3, '\n')
        else:
            npt.assert_equal(result3, "")

    # Make some assignments and run basic operations
    def test_basic_operation(self):
        result_assignment_a = self.mlab.run_code("a = 21.23452261")['content']['stdout']
        result_assignment_b = self.mlab.run_code("b = 347.745")['content']['stdout']
        result_sum = self.mlab.run_code("a + b")['content']['stdout']
        result_diff = self.mlab.run_code("a - b")['content']['stdout']
        result_product = self.mlab.run_code("a * b")['content']['stdout']
        result_division = self.mlab.run_code("c = a / b")['content']['stdout']

        if tu.on_octave():
            npt.assert_equal(result_assignment_a, text_type("a =  21.235\n"))
            npt.assert_equal(result_assignment_b, text_type("b =  347.75\n"))
            npt.assert_equal(result_sum, text_type("ans =  368.98\n"))
            npt.assert_equal(result_diff, text_type("ans = -326.51\n"))
            npt.assert_equal(result_product, text_type("ans =  7384.2\n"))
            npt.assert_equal(result_division, text_type("c =  0.061063\n"))
        else:
            npt.assert_equal(result_assignment_a, text_type("\na =\n\n   21.2345\n\n"))
            npt.assert_equal(result_assignment_b, text_type("\nb =\n\n  347.7450\n\n"))
            npt.assert_equal(result_sum, text_type("\nans =\n\n  368.9795\n\n"))
            npt.assert_equal(result_diff, text_type("\nans =\n\n -326.5105\n\n"))
            npt.assert_equal(result_product, text_type("\nans =\n\n   7.3842e+03\n\n"))
            npt.assert_equal(result_division, text_type("\nc =\n\n    0.0611\n\n"))

    # Put in some undefined code
    def test_undefined_code(self):
        success = self.mlab.run_code("this_is_nonsense")['success']
        message = self.mlab.run_code("this_is_nonsense")['content']['stdout']

        npt.assert_equal(success, "false")
        if tu.on_octave():
            npt.assert_equal(message, "'this_is_nonsense' undefined near line 1 column 1")
        else:
            npt.assert_equal(message, "Undefined function or variable 'this_is_nonsense'.")


    def test_nargout(self):
        res  = self.mlab.run_func('svd', np.array([[1,2],[1,3]]), nargout=3)
        U, S, V = res['result']
        npt.assert_almost_equal(U, np.array([[-0.57604844, -0.81741556],
                                             [-0.81741556, 0.57604844]]))

        npt.assert_almost_equal(S, np.array([[ 3.86432845, 0.],
                                             [ 0., 0.25877718]]))

        npt.assert_almost_equal(V, np.array([[-0.36059668, -0.93272184],
                                             [-0.93272184, 0.36059668]]))

        res = self.mlab.run_func('svd', np.array([[1,2],[1,3]]), nargout=1)
        s = res['result']
        npt.assert_almost_equal(s, [[ 3.86432845], [ 0.25877718]])

        res = self.mlab.run_func('close', 'all', nargout=0)
        assert res['result'] == []

    def test_tuple_args(self):
        res = self.mlab.run_func('ones', (1, 2))
        npt.assert_almost_equal(res['result'], [[1, 1]])

        res = self.mlab.run_func('chol',
                                 (np.array([[2, 2], [1, 1]]), 'lower'))
        npt.assert_almost_equal(res['result'],
                                [[1.41421356, 0.],
                                 [0.70710678, 0.70710678]])
