# CMake generated Testfile for 
# Source directory: /home/ubuntu/catkin_ws/src/geographic_info/geodesy
# Build directory: /home/ubuntu/catkin_ws/build/geographic_info/geodesy
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_geodesy_gtest_test_wgs84 "/home/ubuntu/catkin_ws/build/catkin_generated/env_cached.sh" "/usr/bin/python" "/opt/ros/indigo/share/catkin/cmake/test/run_tests.py" "/home/ubuntu/catkin_ws/build/test_results/geodesy/gtest-test_wgs84.xml" "--return-code" "/home/ubuntu/catkin_ws/devel/lib/geodesy/test_wgs84 --gtest_output=xml:/home/ubuntu/catkin_ws/build/test_results/geodesy/gtest-test_wgs84.xml")
add_test(_ctest_geodesy_gtest_test_utm "/home/ubuntu/catkin_ws/build/catkin_generated/env_cached.sh" "/usr/bin/python" "/opt/ros/indigo/share/catkin/cmake/test/run_tests.py" "/home/ubuntu/catkin_ws/build/test_results/geodesy/gtest-test_utm.xml" "--return-code" "/home/ubuntu/catkin_ws/devel/lib/geodesy/test_utm --gtest_output=xml:/home/ubuntu/catkin_ws/build/test_results/geodesy/gtest-test_utm.xml")
add_test(_ctest_geodesy_nosetests_tests.test_bounding_box.py "/home/ubuntu/catkin_ws/build/catkin_generated/env_cached.sh" "/usr/bin/python" "/opt/ros/indigo/share/catkin/cmake/test/run_tests.py" "/home/ubuntu/catkin_ws/build/test_results/geodesy/nosetests-tests.test_bounding_box.py.xml" "--return-code" "/usr/bin/cmake -E make_directory /home/ubuntu/catkin_ws/build/test_results/geodesy" "/usr/bin/nosetests-2.7 -P --process-timeout=60 /home/ubuntu/catkin_ws/src/geographic_info/geodesy/tests/test_bounding_box.py --with-xunit --xunit-file=/home/ubuntu/catkin_ws/build/test_results/geodesy/nosetests-tests.test_bounding_box.py.xml")
add_test(_ctest_geodesy_nosetests_tests.test_props.py "/home/ubuntu/catkin_ws/build/catkin_generated/env_cached.sh" "/usr/bin/python" "/opt/ros/indigo/share/catkin/cmake/test/run_tests.py" "/home/ubuntu/catkin_ws/build/test_results/geodesy/nosetests-tests.test_props.py.xml" "--return-code" "/usr/bin/cmake -E make_directory /home/ubuntu/catkin_ws/build/test_results/geodesy" "/usr/bin/nosetests-2.7 -P --process-timeout=60 /home/ubuntu/catkin_ws/src/geographic_info/geodesy/tests/test_props.py --with-xunit --xunit-file=/home/ubuntu/catkin_ws/build/test_results/geodesy/nosetests-tests.test_props.py.xml")
add_test(_ctest_geodesy_nosetests_tests.test_utm.py "/home/ubuntu/catkin_ws/build/catkin_generated/env_cached.sh" "/usr/bin/python" "/opt/ros/indigo/share/catkin/cmake/test/run_tests.py" "/home/ubuntu/catkin_ws/build/test_results/geodesy/nosetests-tests.test_utm.py.xml" "--return-code" "/usr/bin/cmake -E make_directory /home/ubuntu/catkin_ws/build/test_results/geodesy" "/usr/bin/nosetests-2.7 -P --process-timeout=60 /home/ubuntu/catkin_ws/src/geographic_info/geodesy/tests/test_utm.py --with-xunit --xunit-file=/home/ubuntu/catkin_ws/build/test_results/geodesy/nosetests-tests.test_utm.py.xml")
add_test(_ctest_geodesy_nosetests_tests.test_wu_point.py "/home/ubuntu/catkin_ws/build/catkin_generated/env_cached.sh" "/usr/bin/python" "/opt/ros/indigo/share/catkin/cmake/test/run_tests.py" "/home/ubuntu/catkin_ws/build/test_results/geodesy/nosetests-tests.test_wu_point.py.xml" "--return-code" "/usr/bin/cmake -E make_directory /home/ubuntu/catkin_ws/build/test_results/geodesy" "/usr/bin/nosetests-2.7 -P --process-timeout=60 /home/ubuntu/catkin_ws/src/geographic_info/geodesy/tests/test_wu_point.py --with-xunit --xunit-file=/home/ubuntu/catkin_ws/build/test_results/geodesy/nosetests-tests.test_wu_point.py.xml")
