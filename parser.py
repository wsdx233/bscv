import re
from datetime import datetime

def parse_log(log_path):
    """
    解析聊天日志文件。
    """
    chat_messages = []
    # 正则表达式
    msg_pattern = re.compile(r"^(?P<timestamp>\w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4}) (?P<user>.+?) cid-?\d+:(?P<message>.*)$")
    info_pattern = re.compile(r"^(?P<user_display>.+?)\((?P<user_id>pb-.+?)\)'s info: (?P<info_dict>\{.*\})$")

    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                msg_match = msg_pattern.match(line)
                
                if msg_match:
                    msg_data = msg_match.groupdict()
                    message_content = msg_data['message'].strip()
                    
                    if not message_content:
                        i += 1
                        continue

                    user_info = {
                        'user_id': None,
                        'v2_name': None,
                        'user_type': 'Local'
                    }

                    # 检查下一行是否是用户信息
                    if i + 1 < len(lines):
                        info_match = info_pattern.match(lines[i + 1].strip())
                        if info_match:
                            info_data = info_match.groupdict()
                            try:
                                info_dict = eval(info_data['info_dict'])
                                user_info['user_id'] = info_data['user_id']
                                user_info['v2_name'] = info_dict.get('n')
                                user_info['user_type'] = info_dict.get('a', 'Local')
                            except:
                                pass # 如果eval失败则忽略
                            i += 1 # 跳过信息行

                    chat_messages.append({
                        'timestamp': datetime.strptime(msg_data['timestamp'], '%a %b %d %H:%M:%S %Y'),
                        'user': msg_data['user'].strip(),
                        'message': message_content,
                        'user_id': user_info['user_id'],
                        'v2_name': user_info['v2_name'],
                        'user_type': user_info['user_type']
                    })
                i += 1

    except FileNotFoundError:
        print(f"错误: 聊天日志文件未找到 at path: {log_path}")
        return []
        
    return chat_messages

if __name__ == '__main__':
    # 用于测试
    import config
    messages = parse_log(config.CHAT_LOG_PATH)
    for msg in messages:
        print(msg)