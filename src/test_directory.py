import unittest
import directory

ROOT = "C:\\easyfox_test"
JSON = r'{"exists": true, "parent": "C:\\", "name": "easyfox_test", "stem": "easyfox_test", "suffix": "", "full_path": "C:\\easyfox_test", "is_dir": true, "is_file": false, "depth": 0, "has_children": true, "count_children": 2, "children": [{"exists": true, "parent": "C:\\easyfox_test", "name": "dir", "stem": "dir", "suffix": "", "full_path": "C:\\easyfox_test\\dir", "is_dir": true, "is_file": false, "depth": 1, "has_children": true, "count_children": 2, "children": [{"exists": true, "parent": "C:\\easyfox_test\\dir", "name": "dir2", "stem": "dir2", "suffix": "", "full_path": "C:\\easyfox_test\\dir\\dir2", "is_dir": true, "is_file": false, "depth": 2, "has_children": true, "count_children": 2, "children": [{"exists": true, "parent": "C:\\easyfox_test\\dir\\dir2", "name": "dir3", "stem": "dir3", "suffix": "", "full_path": "C:\\easyfox_test\\dir\\dir2\\dir3", "is_dir": true, "is_file": false, "depth": 3, "has_children": false, "count_children": 0, "children": []}, {"exists": true, "parent": "C:\\easyfox_test\\dir\\dir2", "name": "test3.txt", "stem": "test3", "suffix": ".txt", "full_path": "C:\\easyfox_test\\dir\\dir2\\test3.txt", "is_dir": false, "is_file": true, "depth": 3, "has_children": false, "count_children": 0, "children": []}]}, {"exists": true, "parent": "C:\\easyfox_test\\dir", "name": "test2.txt", "stem": "test2", "suffix": ".txt", "full_path": "C:\\easyfox_test\\dir\\test2.txt", "is_dir": false, "is_file": true, "depth": 2, "has_children": false, "count_children": 0, "children": []}]}, {"exists": true, "parent": "C:\\easyfox_test", "name": "test.txt", "stem": "test", "suffix": ".txt", "full_path": "C:\\easyfox_test\\test.txt", "is_dir": false, "is_file": true, "depth": 1, "has_children": false, "count_children": 0, "children": []}]}'


class TestDirectory(unittest.TestCase):
    def test_init(self):
        dir_tree = directory.DirTree(ROOT)
        self.assertTrue(dir_tree.exists)

    def test_str(self):
        dir_tree = directory.DirTree(ROOT)
        self.assertEqual(str(dir_tree), ROOT)

    def test_to_json(self):
        dir_tree = directory.DirTree(ROOT)
        self.assertEqual(dir_tree.to_JSON(), JSON)


if __name__ == '__main__':
    unittest.main()
