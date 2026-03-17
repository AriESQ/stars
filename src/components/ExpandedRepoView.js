import React from 'react';

const ExpandedRepoView = ({ repo, name }) => {
  return (
    <div className="px-6 py-4 border-t border-gray-100">
      <p className="text-gray-700 mb-2">{repo.metadata.description}</p>
      <p className="text-sm text-gray-600 mb-2">Language: {repo.metadata.language}</p>
      <p className="text-sm text-gray-600 mb-2">Created: {new Date(repo.metadata.created_at).toLocaleDateString()}</p>
      <p className="text-sm text-gray-600 mb-2">Last updated: {new Date(repo.metadata.updated_at).toLocaleDateString()}</p>
      <p className="text-sm text-gray-600 mb-2">Last pushed: {new Date(repo.metadata.pushed_at).toLocaleDateString()}</p>
      <p className="text-sm text-gray-600 mb-2">Starred at: {new Date(repo.metadata.starred_at).toLocaleDateString()}</p>
      {repo.lists && repo.lists.length > 0 && (
        <p className="text-sm text-gray-600 mb-2">Lists: {repo.lists.join(', ')}</p>
      )}
    </div>
  );
};

export default ExpandedRepoView;
