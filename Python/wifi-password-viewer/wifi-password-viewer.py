import subprocess

# Return saved Wi-Fi profile name
def get_wifi_profiles():
    output = subprocess.check_output(
        ["netsh", "wlan", "show", "profiles"],
        text=True,    # output gives you a normal string
        encoding="utf-8",
        errors="ignore"
    )

    profiles = []

    for line in output.splitlines():
        if "All User Profiles" in line:
            name = line.split(":", 1)[1].strip()
            profiles.append(name)

    return profiles

# Return the saved password for a Wi-Fi profile
def get_wifi_password(profile):
    output = subprocess.check_output(
        ["netsh", "wlan", "show",  "profile", profile, "key=clear"],
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    for line in output.splitlines():
        if "Key Content" in line:
            return line.split(":", 1)[1].strip()

    return "Password not available"


def main():
    profiles = get_wifi_profiles()

    if not profiles:
        print("No saved Wi-Fi profiles found.")
        return

    print("\nSaved Wi-Fi Networks")
    print("-" * 30)

    for index, profile in enumerate(profiles, start=1):
        print(f"[{index}] {profile}")

    try:
        choice = int(input("\nChoose Wi-Fi number: "))
        if choice < 1 or choice > len(profiles):
            print("Invalid Wi-Fi number.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    selected_profile = profiles[choice - 1]
    password = get_wifi_password(selected_profile)

    print("\nWi-Fi Information")
    print("-" * 30)
    print(f"Network: {selected_profile}")
    print(f"Password: {password}")

if __name__ == "__main__":
    main()
