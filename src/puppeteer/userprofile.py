from getpass import getuser
from pathlib import Path
from typing import Optional


def profile_dir() -> Optional[str]:
    user = getuser()
    profiles_dir = f"C:\\Users\\{user}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"
    p = Path(profiles_dir)
    if p.is_dir():
        for profile in p.iterdir():
            if profile.is_dir():
                if "default" in profile.name.lower():
                    return str(profile)
    return None

# PROFILE = "C:\\Users\\s150209\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\5332jmf7.default"  # 会社PC
# PROFILE = "C:\\Users\\Tomoyuki Nakamura\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\2wsrx870.Default User"  # 自宅PC
