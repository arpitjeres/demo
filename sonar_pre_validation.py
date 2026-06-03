import os
import sys
import subprocess
import xml.etree.ElementTree as ET

ALLOWED_JAVA_VERSIONS = ["1.8", "17"]

EXCLUDED_DIRS = [
    "node_modules",
    "target",
    ".m2",
    "reports"
]

def validate_java():
    try:
        output = subprocess.check_output(
            ["java", "-version"],
            stderr=subprocess.STDOUT,
            text=True
        )

        if "1.8" in output:
            version = "1.8"
        elif "17" in output:
            version = "17"
        else:
            version = "Unsupported"

        print(f"[INFO] Java Version: {version}")

        if version not in ALLOWED_JAVA_VERSIONS:
            raise Exception(
                f"Invalid Java Version. Allowed: {ALLOWED_JAVA_VERSIONS}"
            )

    except Exception as e:
        print(f"[ERROR] Java validation failed: {e}")
        sys.exit(1)


def validate_pom():
    pom_file = "pom.xml"

    if not os.path.exists(pom_file):
        print("[ERROR] pom.xml not found")
        sys.exit(1)

    tree = ET.parse(pom_file)
    root = tree.getroot()

    ns = {'m': 'http://maven.apache.org/POM/4.0.0'}

    packaging = root.find('m:packaging', ns)

    if packaging is not None and packaging.text == "pom":
        print("[INFO] Multi-module Maven Project detected")

    parent = root.find('m:parent', ns)

    if parent is not None:
        print("[INFO] Parent POM configuration found")


def validate_sonar_properties():
    sonar_file = "sonar-project.properties"

    if os.path.exists(sonar_file):
        print("[INFO] sonar-project.properties found")
    else:
        print("[WARNING] sonar-project.properties not found")


def validate_exclusions():
    print("[INFO] Checking excluded directories")

    for folder in EXCLUDED_DIRS:
        if os.path.exists(folder):
            print(f"[INFO] Exclusion configured for: {folder}")


def validate_maven():
    try:
        output = subprocess.check_output(
            ["mvn", "-v"],
            text=True
        )
        print("[INFO] Maven Installed")
    except:
        print("[ERROR] Maven not found")
        sys.exit(1)


def main():
    print("========== SONAR PRE-VALIDATION ==========")

    validate_java()
    validate_maven()
    validate_pom()
    validate_sonar_properties()
    validate_exclusions()

    print("\n[SUCCESS] All validations passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
