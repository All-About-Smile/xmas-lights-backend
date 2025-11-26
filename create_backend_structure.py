import os

# 생성할 디렉토리 구조 정의
structure = {
    "backend": {
        "app": {
            "api": {
                "__init__.py": "",
                "auth.py": "",
                "capsule.py": "",
                "public.py": "",
                "letters.py": "",
            },
            "core": {
                "__init__.py": "",
                "config.py": "",
                "security.py": "",
                "timecheck.py": "",
            },
            "db": {
                "__init__.py": "",
                "base.py": "",
                "session.py": "",
                "models": {
                    "__init__.py": "",
                    "user.py": "",
                    "capsule.py": "",
                    "letter.py": "",
                },
            },
            "schemas": {
                "__init__.py": "",
                "auth_schema.py": "",
                "user_schema.py": "",
                "capsule_schema.py": "",
                "letter_schema.py": "",
                "public_schema.py": "",
            },
            "services": {
                "__init__.py": "",
                "auth_service.py": "",
                "capsule_service.py": "",
                "letter_service.py": "",
                "public_service.py": "",
            },
            "utils": {
                "__init__.py": "",
                "token.py": "",
                "password.py": "",
            },
            "main.py": "",
        },
        "tests": {
            "__init__.py": "",
            "test_auth.py": "",
            "test_public.py": "",
            "test_letters.py": "",
        },
        ".env": "",
        "requirements.txt": "",
        "README.md": "",
    }
}


def create_structure(base_path, structure_dict):
    for name, content in structure_dict.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            # 디렉토리 생성
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            # 파일 생성
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


if __name__ == "__main__":
    create_structure(".", structure)
    print("🎉 FastAPI Backend directory structure created successfully!")
