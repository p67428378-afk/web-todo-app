/**
 * Module: localStorage
 * Purpose: Utility functions for interacting with browser local storage.
 * Author: Developer_Agent
 * Created: 2026-02-27
 * Notes: Handles saving and loading of to-do items.
 */

const TODO_STORAGE_KEY = 'web-todo-app-tasks';

/**
 * Loads tasks from local storage.
 * @returns {Array<Object>} An array of task objects.
 */
export const load_tasks = () => {
  try {
    const serialized_tasks = localStorage.getItem(TODO_STORAGE_KEY);
    if (serialized_tasks === null) {
      return [];
    }
    return JSON.parse(serialized_tasks);
  } catch (error) {
    console.error("Error loading tasks from local storage:", error);
    return [];
  }
};

/**
 * Saves tasks to local storage.
 * @param {Array<Object>} tasks - An array of task objects to save.
 */
export const save_tasks = (tasks) => {
  try {
    const serialized_tasks = JSON.stringify(tasks);
    localStorage.setItem(TODO_STORAGE_KEY, serialized_tasks);
  } catch (error) {
    console.error("Error saving tasks to local storage:", error);
  }
};
