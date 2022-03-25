import Navbar from './components/navbar';
import Table from './components/table';

export function App() {
  localStorage.setItem('theme', 'dark');

  return (
    <div className="relative flex flex-col w-full h-full">
      <Navbar />
      <div className="flex-grow self-center pt-24">
        <p class="text-3xl dark:text-white pb-4 mb-6 border-b-2 border-green-400 rounded-b">
          Gestión de usuarios
        </p>
        <Table />
      </div>
    </div>
  );
}
