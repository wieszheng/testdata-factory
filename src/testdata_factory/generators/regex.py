"""自定义正则规则生成器"""

import random
import re
import string
from typing import Any


# 字符集映射
CHAR_SETS = {
    'd': string.digits,
    'w': string.ascii_letters + string.digits + '_',
    'a': string.ascii_lowercase,
    'A': string.ascii_uppercase,
    's': ' \t\n\r\f\v',
    '.': string.printable,
}


def _parse_char_class(pattern: str, pos: int) -> tuple[str, int]:
    """
    解析字符类 [...] 
    
    Returns:
        (允许的字符集, 结束位置)
    """
    chars = ""
    negate = False
    pos += 1  # 跳过 [
    
    if pos < len(pattern) and pattern[pos] == '^':
        negate = True
        pos += 1
    
    while pos < len(pattern) and pattern[pos] != ']':
        if pos + 2 < len(pattern) and pattern[pos + 1] == '-':
            # 范围 a-z
            start = pattern[pos]
            end = pattern[pos + 2]
            chars += ''.join(chr(c) for c in range(ord(start), ord(end) + 1))
            pos += 3
        else:
            chars += pattern[pos]
            pos += 1
    
    if negate:
        # 排除指定字符
        all_chars = string.printable
        chars = ''.join(c for c in all_chars if c not in chars)
    
    return chars, pos + 1


def _generate_from_pattern(pattern: str) -> str:
    """
    根据简化正则模式生成字符串
    
    支持:
    - \d: 数字
    - \w: 字母数字下划线
    - \a: 小写字母
    - \A: 大写字母
    - [abc]: 字符类
    - [a-z]: 范围
    - {n}: 重复 n 次
    - {n,m}: 重复 n-m 次
    - *: 0-n 次
    - +: 1-n 次
    - ?: 0-1 次
    - .: 任意字符
    - |: 或（随机选择）
    - (abc): 分组
    """
    result = []
    i = 0
    
    while i < len(pattern):
        char = pattern[i]
        
        if char == '\\':
            # 转义字符
            if i + 1 < len(pattern):
                next_char = pattern[i + 1]
                if next_char == 'd':
                    result.append(random.choice(string.digits))
                elif next_char == 'w':
                    result.append(random.choice(string.ascii_letters + string.digits + '_'))
                elif next_char == 'a':
                    result.append(random.choice(string.ascii_lowercase))
                elif next_char == 'A':
                    result.append(random.choice(string.ascii_uppercase))
                elif next_char == 's':
                    result.append(random.choice(' \t'))
                elif next_char in CHAR_SETS:
                    result.append(random.choice(CHAR_SETS[next_char]))
                else:
                    result.append(next_char)
                i += 2
            else:
                i += 1
        
        elif char == '[':
            chars, new_pos = _parse_char_class(pattern, i)
            if chars:
                result.append(random.choice(chars))
            i = new_pos
        
        elif char == '{':
            # 重复次数 {n} 或 {n,m}
            j = i + 1
            while j < len(pattern) and pattern[j] != '}':
                j += 1
            
            if j < len(pattern):
                count_str = pattern[i+1:j]
                if ',' in count_str:
                    min_count, max_count = count_str.split(',')
                    min_count = int(min_count) if min_count else 0
                    max_count = int(max_count) if max_count else min_count + 10
                    repeat = random.randint(min_count, max_count)
                else:
                    repeat = int(count_str)
                
                # 重复前一个字符/组
                if result:
                    last = result.pop()
                    result.append(last * repeat)
            
            i = j + 1
        
        elif char == '*':
            # 0-n 次重复
            if result:
                last = result.pop()
                repeat = random.randint(0, 5)
                result.append(last * repeat)
            i += 1
        
        elif char == '+':
            # 1-n 次重复
            if result:
                last = result.pop()
                repeat = random.randint(1, 5)
                result.append(last * repeat)
            i += 1
        
        elif char == '?':
            # 0-1 次
            if result:
                last = result.pop()
                if random.random() < 0.5:
                    result.append(last)
            i += 1
        
        elif char == '.':
            result.append(random.choice(string.ascii_letters + string.digits))
            i += 1
        
        elif char == '|':
            # 或 - 随机选择之前或之后
            # 简化处理：随机决定是否保留之前的结果
            if result and random.random() < 0.5:
                pass  # 保留
            i += 1
        
        elif char == '(':
            # 找到对应的 )
            depth = 1
            j = i + 1
            while j < len(pattern) and depth > 0:
                if pattern[j] == '(':
                    depth += 1
                elif pattern[j] == ')':
                    depth -= 1
                j += 1
            
            # 递归处理分组内容
            group_content = pattern[i+1:j-1]
            result.append(_generate_from_pattern(group_content))
            i = j
        
        else:
            result.append(char)
            i += 1
    
    return ''.join(result)


def generate_from_regex(pattern: str) -> str:
    """
    根据正则表达式生成匹配的字符串
    
    注意：这是一个简化的实现，不支持所有正则特性。
    支持的格式：
    - \d: 数字
    - \w: 字母数字下划线
    - [abc], [a-z]: 字符类
    - {n}, {n,m}: 重复次数
    - *, +, ?: 量词
    - .: 任意字符
    - 普通字符: 原样输出
    
    Args:
        pattern: 简化的正则表达式
        
    Returns:
        生成的字符串
    """
    return _generate_from_pattern(pattern)


# 预定义规则模板
REGEX_TEMPLATES = {
    "手机号": r"1[3-9]\d{9}",
    "邮箱": r"[a-z]{3,8}\d{2,4}@(qq|163|126|gmail)\.com",
    "身份证号": r"[1-9]\d{5}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]",
    "IP地址": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
    "车牌号": r"[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼][A-Z][A-HJ-NP-Z0-9]{5,6}",
    "统一社会信用代码": r"[0-9A-HJ-NPQRTUWXY]{2}\d{6}[0-9A-HJ-NPQRTUWXY]{10}",
    "银行卡号": r"6[2-5]\d{14,17}",
    "用户名": r"[a-zA-Z][a-zA-Z0-9_]{5,15}",
    "密码": r"[a-zA-Z0-9!@#$%^&*]{8,16}",
    "订单号": r"ORD\d{14}",
    "流水号": r"[A-Z]{2}\d{12}",
}


def get_template(name: str) -> str | None:
    """获取预定义模板"""
    return REGEX_TEMPLATES.get(name)


def list_templates() -> dict[str, str]:
    """列出所有预定义模板"""
    return REGEX_TEMPLATES.copy()
