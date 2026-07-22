export default function RecipeSkeleton({ count = 6 }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="bg-white dark:bg-gray-800 rounded-2xl overflow-hidden shadow-card">
          <div className="h-48 skeleton" />
          <div className="p-4 space-y-3">
            <div className="h-4 skeleton rounded w-1/3" />
            <div className="h-5 skeleton rounded w-2/3" />
            <div className="h-4 skeleton rounded w-full" />
            <div className="h-4 skeleton rounded w-1/2" />
          </div>
        </div>
      ))}
    </div>
  );
}
