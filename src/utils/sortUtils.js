export const fieldOptions = [
  { value: 'name', label: 'Name' },
  { value: 'description', label: 'Description' },
  { value: 'language', label: 'Language' },
  { value: 'stars', label: 'Stars' },
  { value: 'created_at', label: 'Created At' },
  { value: 'updated_at', label: 'Updated At' },
  { value: 'pushed_at', label: 'Pushed At' },
  { value: 'starred_at', label: 'Starred At' },
  { value: 'lists', label: 'Lists' },
];

export const getOperators = (fieldType) => {
  switch (fieldType) {
    case 'string':
      return [
        { value: 'contains', label: 'contains' },
        { value: 'equals', label: 'equals' },
        { value: 'starts_with', label: 'starts with' },
        { value: 'ends_with', label: 'ends with' },
      ];
    case 'number':
      return [
        { value: 'equals', label: 'equals' },
        { value: 'greater_than', label: 'greater than' },
        { value: 'less_than', label: 'less than' },
      ];
    case 'date':
      return [
        { value: 'equals', label: 'equals' },
        { value: 'after', label: 'after' },
        { value: 'before', label: 'before' },
      ];
    case 'list':
      return [
        { value: 'includes', label: 'includes' },
        { value: 'excludes', label: 'excludes' },
      ];
    default:
      return [{ value: 'equals', label: 'equals' }];
  }
};

export const getInputType = (field) => {
  switch (field) {
    case 'stars':
      return 'number';
    case 'created_at':
    case 'updated_at':
    case 'pushed_at':
    case 'starred_at':
      return 'date';
    case 'lists':
      return 'list';
    default:
      return 'text';
  }
};
