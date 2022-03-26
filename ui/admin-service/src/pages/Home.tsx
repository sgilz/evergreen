import { FunctionalComponent } from 'preact'
import { useEffect, useState } from 'preact/hooks';
import Table from '../components/table';

const Home: FunctionalComponent = () => {
    const [show, setShow] = useState(false);
    const queryString = window.location.search;
    const query = new URLSearchParams(queryString);

    useEffect(() => {
      if (!localStorage.getItem('token')) {
        if (query.get('token')) {
          localStorage.setItem('token', (query.get('token') as string))
          setShow(true)
        } else {
          window.location.href = `${(import.meta.env['VITE_LOGIN_APP'] as string)}?origin=signout`
        }
      } else {
          setShow(true)
      }

      if (query.get('token')) {
        history.pushState(null, '', (import.meta.env.BASE_URL as string))
      }
    }, [])

    return (<>{show ?
        <div className="flex-grow self-center pt-24">
            <p class="text-3xl dark:text-white pb-4 mb-6 border-b-2 border-green-400 rounded-b">
                Gestión de usuarios
            </p>
            <Table />
        </div>
        :
        <></>
        }
    </>)
}

export default Home;