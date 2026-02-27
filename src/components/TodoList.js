/**
 * Module: TodoList
 * Purpose: React component for managing and displaying a list of to-do items.
 * Author: Developer_Agent
 * Created: 2026-02-27
 * Notes: Integrates with local storage for persistence.
 */

import React, { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import TodoItem from './TodoItem';
import { load_tasks, save_tasks } from '../utils/localStorage';

/**
 * TodoList component manages the state and display of to-do items.
 * @returns {JSX.Element}
 */
const TodoList = () => {
  const [tasks, set_tasks] = useState([]);
  const [new_task_description, set_new_task_description] = useState('');

  useEffect(() => {
    set_tasks(load_tasks());
  }, []);

  useEffect(() => {
    save_tasks(tasks);
  }, [tasks]);

  const handle_add_task = (event) => {
    event.preventDefault();
    if (new_task_description.trim() === '') return;

    const new_task = {
      id: uuidv4(),
      description: new_task_description.trim(),
      done: false,
    };
    set_tasks((prev_tasks) => [...prev_tasks, new_task]);
    set_new_task_description('');
  };

  const handle_toggle_done = (id) => {
    set_tasks((prev_tasks) =>
      prev_tasks.map((task) =>
        task.id === id ? { ...task, done: !task.done } : task
      )
    );
  };

  const handle_delete_task = (id) => {
    set_tasks((prev_tasks) => prev_tasks.filter((task) => task.id !== id));
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-4xl font-bold text-center text-gray-800 mb-8">To-Do List</h1>
      <form onSubmit={handle_add_task} className="flex mb-4">
        <input
          type="text"
          className="flex-1 p-3 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={new_task_description}
          onChange={(e) => set_new_task_description(e.target.value)}
          placeholder="Add a new task..."
        />
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-r-lg transition duration-300"
        >
          Add Task
        </button>
      </form>
      {
        tasks.length === 0 ? (
          <p className="text-center text-gray-500 text-lg">No tasks yet! Add one above.</p>
        ) : (
          <ul className="space-y-3">
            {tasks.map((task) => (
              <TodoItem
                key={task.id}
                todo={task}
                on_toggle_done={handle_toggle_done}
                on_delete={handle_delete_task}
              />
            ))}
          </ul>
        )
      }
    </div>
  );
};

export default TodoList;
