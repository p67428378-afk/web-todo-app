/**
 * Module: TodoItem
 * Purpose: React component for displaying a single to-do item.
 * Author: Developer_Agent
 * Created: 2026-02-27
 * Notes: Allows marking as done and deleting tasks.
 */

import React from 'react';

/**
 * TodoItem component displays a single to-do item.
 * @param {object} props - The component props.
 * @param {object} props.todo - The to-do item object.
 * @param {function} props.on_toggle_done - Function to call when toggling the done status.
 * @param {function} props.on_delete - Function to call when deleting the item.
 * @returns {JSX.Element}
 */
const TodoItem = ({ todo, on_toggle_done, on_delete }) => {
  return (
    <li className="flex items-center justify-between p-3 bg-white rounded-lg shadow mb-3">
      <span
        className={`flex-1 text-lg ${todo.done ? 'line-through text-gray-500' : 'text-gray-900'}`}
      >
        {todo.description}
      </span>
      <div className="flex items-center space-x-2">
        <button
          onClick={() => on_toggle_done(todo.id)}
          className={`py-1 px-3 rounded-md text-sm font-medium ${todo.done ? 'bg-yellow-500 hover:bg-yellow-600 text-white' : 'bg-green-500 hover:bg-green-600 text-white'}`}
        >
          {todo.done ? 'Undo' : 'Done'}
        </button>
        <button
          onClick={() => on_delete(todo.id)}
          className="py-1 px-3 rounded-md text-sm font-medium bg-red-500 hover:bg-red-600 text-white"
        >
          Delete
        </button>
      </div>
    </li>
  );
};

export default TodoItem;
