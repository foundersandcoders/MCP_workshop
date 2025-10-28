# Clean Python code example for testing code review tools
# This file demonstrates good coding practices

from typing import List, Optional


def calculate_sum(numbers: List[int]) -> int:
    """Calculate the sum of a list of numbers."""
    return sum(numbers)


def find_max(numbers: List[int]) -> Optional[int]:
    """Find the maximum number in a list."""
    if not numbers:
        return None
    return max(numbers)


class UserRepository:
    """Repository for managing user data."""

    def __init__(self):
        """Initialize the user repository."""
        self._users = []

    def add_user(self, name: str, email: str) -> bool:
        """Add a new user to the repository."""
        if not name or not email:
            return False

        if self._user_exists(email):
            return False

        user = {"name": name, "email": email}
        self._users.append(user)
        return True

    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get a user by their email address."""
        for user in self._users:
            if user["email"] == email:
                return user
        return None

    def _user_exists(self, email: str) -> bool:
        """Check if a user with the given email already exists."""
        return self.get_user_by_email(email) is not None


def main():
    """Main function to demonstrate the code."""
    numbers = [1, 2, 3, 4, 5]
    print(f"Sum: {calculate_sum(numbers)}")
    print(f"Max: {find_max(numbers)}")

    repo = UserRepository()
    repo.add_user("Alice", "alice@example.com")
    user = repo.get_user_by_email("alice@example.com")
    print(f"User found: {user}")


if __name__ == "__main__":
    main()