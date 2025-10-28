// Clean JavaScript code example for testing code review tools
// This file demonstrates good coding practices

/**
 * Calculate the sum of an array of numbers
 * @param {number[]} numbers - Array of numbers to sum
 * @returns {number} The sum of all numbers
 */
function calculateSum(numbers) {
    if (!Array.isArray(numbers)) {
        throw new Error('Input must be an array');
    }
    return numbers.reduce((sum, num) => sum + num, 0);
}

/**
 * Find the maximum number in an array
 * @param {number[]} numbers - Array of numbers
 * @returns {number|null} The maximum number or null if array is empty
 */
function findMax(numbers) {
    if (!Array.isArray(numbers) || numbers.length === 0) {
        return null;
    }
    return Math.max(...numbers);
}

/**
 * Repository class for managing user data
 */
class UserRepository {
    /**
     * Initialize the user repository
     */
    constructor() {
        this._users = [];
    }

    /**
     * Add a new user to the repository
     * @param {string} name - User's name
     * @param {string} email - User's email address
     * @returns {boolean} True if user was added successfully
     */
    addUser(name, email) {
        if (!name || !email) {
            return false;
        }

        if (this._userExists(email)) {
            return false;
        }

        const user = { name, email };
        this._users.push(user);
        return true;
    }

    /**
     * Get a user by their email address
     * @param {string} email - Email address to search for
     * @returns {Object|null} User object or null if not found
     */
    getUserByEmail(email) {
        return this._users.find(user => user.email === email) || null;
    }

    /**
     * Check if a user with the given email already exists
     * @param {string} email - Email address to check
     * @returns {boolean} True if user exists
     * @private
     */
    _userExists(email) {
        return this.getUserByEmail(email) !== null;
    }

    /**
     * Get all users in the repository
     * @returns {Object[]} Array of all users
     */
    getAllUsers() {
        return [...this._users]; // Return a copy to prevent external modification
    }
}

/**
 * Create a user factory function
 * @param {string} type - Type of user to create
 * @returns {Object} User configuration object
 */
function createUser(type) {
    const userConfigs = {
        admin: { type: 'admin', permissions: ['read', 'write', 'delete'] },
        user: { type: 'user', permissions: ['read'] },
        guest: { type: 'guest', permissions: [] }
    };

    return userConfigs[type] || userConfigs.guest;
}

/**
 * Main function to demonstrate the code
 */
function main() {
    const numbers = [1, 2, 3, 4, 5];
    console.log(`Sum: ${calculateSum(numbers)}`);
    console.log(`Max: ${findMax(numbers)}`);

    const repo = new UserRepository();
    repo.addUser('Alice', 'alice@example.com');
    repo.addUser('Bob', 'bob@example.com');

    const user = repo.getUserByEmail('alice@example.com');
    console.log('User found:', user);

    const adminUser = createUser('admin');
    console.log('Admin config:', adminUser);
}

// Run main function if this file is executed directly
if (typeof require !== 'undefined' && require.main === module) {
    main();
}

module.exports = {
    calculateSum,
    findMax,
    UserRepository,
    createUser
};