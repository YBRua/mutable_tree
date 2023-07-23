import os
import json
import shutil
import subprocess
from tqdm import tqdm
from collections import defaultdict, Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional

import tree_sitter
from dataset_filter import remove_comments
from mutable_tree.adaptors import CppAdaptor, JavaAdaptor, JavaScriptAdaptor
from mutable_tree.stringifiers import (CppStringifier, JavaStringifier,
                                       JavaScriptStringifier)


class MBXPRunner:
    task_prefix = 'MBXP'
    lang = 'txt'

    def __init__(self, source_dir: str, bin_dir: str):
        self.source_dir = source_dir
        self.bin_dir = bin_dir

        self.msg_err_compile = 'Compilation'
        self.msg_err_exec = 'Execution'
        self.msg_good = 'Good'

        self.check_cleanup()

    def _remove_nonempty_dir(self, dir_path: str):
        if os.path.exists(dir_path) and len(os.listdir(dir_path)) > 0:
            print(f'{dir_path} is not empty, removing...')
            shutil.rmtree(dir_path)

    def check_cleanup(self):
        self._remove_nonempty_dir(self.source_dir)
        self._remove_nonempty_dir(self.bin_dir)

        if not os.path.exists(self.source_dir):
            os.makedirs(self.source_dir)
        if not os.path.exists(self.bin_dir):
            os.makedirs(self.bin_dir)

    def _exec(self, cmd: List[str], cwd: Optional[str] = None):
        try:
            exec_result = subprocess.run(
                cmd,
                timeout=15,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=cwd,
            )
            return exec_result.returncode == 0
        except Exception as e:
            print(e)
            return False

    def _compile(self, src_path: str, bin_path: str):
        raise NotImplementedError()

    def _run_ut(self, bin_path: str):
        raise NotImplementedError()

    def _compile_and_check_impl(self, id: str, code: str, src_path: str, bin_path: str):
        compiled = self._compile(src_path, bin_path)
        if not compiled:
            return id, False, self.msg_err_compile + ': ' + src_path

        # run compiled program
        passed = self._run_ut(bin_path)
        if not passed:
            return id, False, self.msg_err_exec + ': ' + src_path

        return id, True, self.msg_good

    def compile_and_check_solution(self, task_id: str, code: str):
        task_name = f'{self.task_prefix}_{task_id}'
        src_path = os.path.join(self.source_dir, f'{task_name}.{self.lang}')
        bin_path = os.path.join(self.bin_dir, f'{task_name}')

        return self._compile_and_check_impl(task_id, code, src_path, bin_path)

    def check_solution_wrapper(self, args):
        return self.compile_and_check_solution(*args)

    def write_code_to_fs(self, instances: List):
        for task_id, code in instances:
            task_name = f'{self.task_prefix}_{task_id}'
            src_path = os.path.join(self.source_dir, f'{task_name}.{self.lang}')
            with open(src_path, 'w', encoding='utf-8') as f:
                f.write(code)

    def check_solutions(self, instances: List, n_processes: int = 1):
        results = []

        self.write_code_to_fs(instances)
        input('NOTE: please manually npm install lodash in the source dir! ')

        with ThreadPoolExecutor(max_workers=n_processes) as executor:
            futures = []
            completion_ids = Counter()
            n_samples = 0

            for instance in instances:
                futures.append(executor.submit(self.check_solution_wrapper, instance))
                completion_ids[instance[0]] += 1
                n_samples += 1

            for future in tqdm(as_completed(futures), total=n_samples):
                result = future.result()
                results.append(result)

        # results = []
        # for instance in tqdm(instances):
        #     results.append(self.check_solution_wrapper(instance))

        res_dict = defaultdict(int)
        failures = set()
        for (id, is_good, msg) in results:
            res_dict[msg.split(':')[0]] += 1
            if not is_good:
                failures.add((id, msg))

        return res_dict, failures


class MBCPPRunner(MBXPRunner):
    task_prefix = 'mbcpp'
    lang = 'cpp'

    def __init__(self, source_dir: str, bin_dir: str):
        super().__init__(source_dir, bin_dir)

    def _compile(self, src_path: str, bin_path: str):
        compiled = self._exec(['g++', src_path, '-o', bin_path])
        return compiled

    def _run_ut(self, bin_path: str):
        passed = self._exec([bin_path])
        return passed


class MBJPRunner(MBXPRunner):
    JDK_BATH_PATH = '/home/borui/.local/usr/lib/jvm/java-8-openjdk-amd64/bin'
    task_prefix = 'mbjp'
    lang = 'java'

    def __init__(self, source_dir: str, bin_dir: str):
        super().__init__(source_dir, bin_dir)

    def _compile(self, src_path: str, bin_path: str):
        javac_path = os.path.join(self.JDK_BATH_PATH, 'javac')
        compiled = self._exec([javac_path, src_path])
        return compiled

    def _run_ut(self, bin_path: str):
        java_path = os.path.join(self.JDK_BATH_PATH, 'java')
        passed = self._exec([java_path, '-cp', bin_path, 'Main'])
        return passed

    def compile_and_check_solution(self, task_id: str, code: str):
        task_name = f'{self.task_prefix}_{task_id}'
        src_path = os.path.join(self.source_dir, task_name, f'main.{self.lang}')
        bin_path = os.path.dirname(src_path)

        if not os.path.exists(bin_path):
            os.makedirs(bin_path)

        return self._compile_and_check_impl(task_id, code, src_path, bin_path)


class MBJSPRunner(MBXPRunner):
    task_prefix = 'mbjsp'
    lang = 'js'

    def __init__(self, source_dir: str, bin_dir: str):
        super().__init__(source_dir, bin_dir)

    def check_cleanup(self):
        super().check_cleanup()

    def _compile(self, src_path: str, bin_path: str):
        return True

    def _run_ut(self, bin_path: str):
        passed = self._exec(['node', bin_path])
        return passed

    def compile_and_check_solution(self, task_id: str, code: str):
        task_name = f'{self.task_prefix}_{task_id}'
        src_path = os.path.join(self.source_dir, f'{task_name}.{self.lang}')

        return self._compile_and_check_impl(task_id, code, src_path, src_path)


def load_samples_with_sol(dataset_path: str):
    with open(dataset_path) as f:
        samples = [json.loads(line) for line in f.readlines()]

    return list(filter(lambda x: x['canonical_solution'] is not None, samples))


def compose_function(sample: Dict) -> str:
    return sample["prompt"] + sample["canonical_solution"]


def compose_function_java(sample: Dict) -> str:
    # remove the closing } for class definition
    sol = sample["canonical_solution"]
    sol = sol.strip().split('\n')[:-1]
    sol = '\n'.join(sol)
    func = sample["prompt"].strip().split('\n')[-1] + '\n' + sol
    return remove_comments(func)


def compose_function_cpp(sample: Dict) -> str:
    func = sample["prompt"].strip().split('\n')[-1] + '\n' + sample["canonical_solution"]
    return remove_comments(func)


def compose_program(sample: Dict) -> str:
    return sample["prompt"] + sample["canonical_solution"] + sample["test"]


def compose_function_javascript(sample: Dict) -> str:
    func = sample["prompt"].strip().split('\n')[-1] + '\n' + sample["canonical_solution"]
    return remove_comments(func)


def _get_java_function_root(root: tree_sitter.Node) -> tree_sitter.Node:
    assert root.type == 'program'
    class_decl_node = root.children[0]
    assert class_decl_node.type == 'class_declaration'
    class_body_node = class_decl_node.children[3]
    assert class_body_node.type == 'class_body'
    func_root_node = class_body_node.children[1]
    assert func_root_node.type == 'method_declaration', func_root_node.type
    return func_root_node


def _get_cpp_function_root(root: tree_sitter.Node) -> tree_sitter.Node:
    assert root.type == 'translation_unit'
    func_root_node = root.children[0]
    assert func_root_node.type == 'function_definition'
    return func_root_node


def _get_javascript_function_root(root: tree_sitter.Node) -> tree_sitter.Node:
    assert root.type == 'program'
    func_root_node = root.children[0]
    assert func_root_node.type == 'function_declaration'
    return func_root_node


def _get_function_root(root: tree_sitter.Node, lang: str) -> tree_sitter.Node:
    if lang == 'java':
        return _get_java_function_root(root)
    elif lang == 'cpp':
        return _get_cpp_function_root(root)
    elif lang == 'javascript':
        return _get_javascript_function_root(root)


def _wrap_code(code: str, lang: str) -> str:
    if lang == 'java':
        return f'public class A {{\n{code}\n}}'
    else:
        return code


def to_mutable_tree(code: str, parser: tree_sitter.Parser, lang: str):
    code = _wrap_code(code, lang)
    tree = parser.parse(code.encode('utf-8'))
    func_root = _get_function_root(tree.root_node, lang)
    if lang == 'java':
        return JavaAdaptor.convert_function_declaration(func_root)
    elif lang == 'cpp':
        return CppAdaptor.convert_function_definition(func_root)
    elif lang == 'javascript':
        return JavaScriptAdaptor.convert_function_declaration(func_root)
    else:
        raise ValueError(f'Unknown language: {lang}')


def round_trip(code: str, parser: tree_sitter.Parser, lang: str):
    mutable_node = to_mutable_tree(code, parser, lang)
    if lang == 'java':
        stringifier = JavaStringifier()
    elif lang == 'cpp':
        stringifier = CppStringifier()
    elif lang == 'javascript':
        stringifier = JavaScriptStringifier()
    else:
        raise ValueError(f'Unknown language: {lang}')
    return stringifier.stringify(mutable_node)


def main():
    LANG = 'javascript'
    MBXP_NAME = {'java': 'mbjp', 'cpp': 'mbcpp', 'javascript': 'mbjsp'}[LANG]
    FILE_STORE = 'mbxp/original/source/'
    BIN_STORE = 'mbxp/original/bin/'
    MBXP_DATASET_PATH = f'datasets/{MBXP_NAME}_release_v1.2_filtered.jsonl'

    if LANG == 'cpp':
        prefix = "#include <bits/stdc++.h>\nusing namespace std;\n"
    elif LANG == 'java':
        prefix = ('import java.io.*;\nimport java.lang.*;\n'
                  'import java.util.*;\nimport java.math.*;\n')
    elif LANG == 'javascript':
        prefix = ''
    else:
        raise RuntimeError(f'Unknown language: {LANG}')

    parser = tree_sitter.Parser()
    lang = tree_sitter.Language('./parser/languages.so', name=LANG)
    parser.set_language(lang)

    samples_with_sol = load_samples_with_sol(MBXP_DATASET_PATH)
    print(f'Number of samples with solution: {len(samples_with_sol)}')

    valid_samples = []
    for sample in samples_with_sol:
        function = compose_program(sample)
        tree = parser.parse(function.encode('utf-8'))
        if tree.root_node.has_error:
            continue
        valid_samples.append(sample)
    print(f'Number of valid samples: {len(valid_samples)}')

    if LANG == 'java':
        runner = MBJPRunner(FILE_STORE, BIN_STORE)
    elif LANG == 'cpp':
        runner = MBCPPRunner(FILE_STORE, BIN_STORE)
    elif LANG == 'javascript':
        runner = MBJSPRunner(FILE_STORE, BIN_STORE)
    else:
        raise ValueError(f'Unknown language: {LANG}')

    # original_instances = []
    # for sample in valid_samples:
    #     program = compose_program(sample)
    #     original_instances.append((sample['task_id'].split('/')[-1], program))
    # res, failures = runner.check_solutions(original_instances, n_processes=16)
    # print(res)
    # print(failures)
    # print()

    # sample_dict = {}
    # for sample in valid_samples:
    #     sample_id = int(sample['task_id'].split('/')[-1])
    #     sample_dict[sample_id] = sample

    # for id, _ in failures:
    #     id = int(id)
    #     sample_dict.pop(id)

    # with open(f'datasets/{MBXP_NAME}_release_v1.2_filtered.jsonl', 'w') as f:
    #     for i in sorted(sample_dict.keys()):
    #         f.write(json.dumps(sample_dict[i]) + '\n')

    # return

    mutableast_instances = []
    for sample in tqdm(valid_samples):
        if LANG == 'cpp':
            function = compose_function_cpp(sample)
        elif LANG == 'java':
            function = compose_function_java(sample)
        elif LANG == 'javascript':
            function = compose_function_javascript(sample)
        else:
            raise ValueError(f'Unknown language: {LANG}')
        try:
            t_function = round_trip(function, parser, LANG)
        except Exception as e:
            print(e)
            continue
        # print(function)
        # t_function = round_trip(function, parser, LANG)

        if LANG == 'java':
            # extract class header
            class_header = sample['prompt'].strip().split('\n')[6]
            t_function = f'{class_header}\n{t_function}\n}}'

        t_program = prefix + t_function + sample["test"]
        task_id = sample['task_id'].split('/')[-1]
        mutableast_instances.append((task_id, t_program))

    res, failures = runner.check_solutions(mutableast_instances, n_processes=16)
    print(res, failures)
    print()


if __name__ == '__main__':
    main()
