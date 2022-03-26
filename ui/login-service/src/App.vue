<script setup lang="ts">
import useVuelidate from '@vuelidate/core';
import LoadingSpinner from './components/LoadingSpinner.vue';
import Toast from './components/Toast.vue';
import { required } from '@vuelidate/validators';
import { onMounted, ref } from 'vue';
import ky from 'ky';
import jwt_decode from 'jwt-decode';

const queryString = window.location.search;
const query = new URLSearchParams(queryString);

onMounted(() => {
  if (query.get('origin') && query.get('origin') === 'signout') {
    localStorage.removeItem('token');
  }
  if (localStorage.getItem('token')) {
    const token = localStorage.getItem('token') as string;
    const user: any = jwt_decode(token);
    if (user.role === 'admin') {
      window.location.href = `${
        import.meta.env['VITE_ADMIN_APP'] as string
      }?token=${token}`;
    } else {
      window.location.href = `${
        import.meta.env['VITE_GUEST_APP'] as string
      }?token=${token}`;
    }
  }
});

const form = ref({
  username: '',
  password: '',
});
const showPassword = ref(false);
const isSubmitting = ref(false);
const isError = ref(false);

const rules: any = {
  username: { required },
  password: { required },
};

const v$ = useVuelidate(rules, form);

const handleSubmit = async () => {
  try {
    isSubmitting.value = true;
    isError.value = false;
    if (!(await v$.value.$validate())) return;
    const res: { token: string } = await ky
      .post((import.meta.env['VITE_API_URL'] as string) + '/login', {
        headers: {
          Authorization:
            'Basic ' + btoa(form.value.username + ':' + form.value.password),
        },
      })
      .json();
    const { token } = res;
    localStorage.setItem('token', token);
    const user: any = jwt_decode(localStorage.getItem('token') as string);
    if (user.role === 'admin') {
      window.location.href = `${
        import.meta.env['VITE_ADMIN_APP'] as string
      }?token=${token}`;
    } else {
      window.location.href = `${
        import.meta.env['VITE_GUEST_APP'] as string
      }?token=${token}`;
    }
  } catch (error) {
    isError.value = true;
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div class="relative pt-24">
    <transition name="toast">
      <toast
        v-if="isError"
        message="Ocurrió un error, inténtalo de nuevo."
        @toast-close="isError = false"
      />
    </transition>
    <div
      class="flex mx-auto max-w-4xl bg-white rounded-lg border border-gray-200 shadow-md dark:bg-gray-800 dark:border-gray-700"
    >
      <img
        src="./assets/farm_picture.jpg"
        alt="Foto de una granja"
        class="object-cover w-full h-96 rounded-t-lg md:h-auto md:w-72 hidden md:block md:rounded-none md:rounded-l-lg"
      />
      <form
        class="space-y-6 px-6 py-12 flex-grow"
        @submit.prevent="handleSubmit"
      >
        <div class="flex justify-evenly items-center divide-x">
          <h5 class="text-xl font-medium text-gray-900 dark:text-white">
            Iniciar Sesión
          </h5>
          <img src="./assets/evergreen.png" alt="Logo Evergreen" class="pl-8" />
        </div>
        <div>
          <label
            for="username"
            class="block text-sm font-medium text-gray-900 dark:text-gray-300"
            >Usuario</label
          >
          <input
            v-model="form.username"
            type="text"
            name="username"
            id="username"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
            :class="
              v$.username.$error
                ? 'focus:ring-red-500 focus:border-red-500'
                : 'focus:ring-blue-500 focus:border-blue-500'
            "
            placeholder="evergreen"
            required
            @blur="v$.username.$touch()"
          />
          <span
            class="text-sm"
            :class="v$.username.$error ? 'text-red-500' : ''"
            >{{ v$.username.$dirty ? (v$.username as any).required.$invalid ? 'El usuario es requerido' : '&nbsp;' : '&nbsp;' }}</span
          >
        </div>
        <div>
          <label
            for="password"
            class="block text-sm font-medium text-gray-900 dark:text-gray-300"
            >Contraseña</label
          >
          <div class="relative">
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              name="password"
              id="password"
              placeholder="••••••••"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
              :class="
                v$.password.$error
                  ? 'focus:ring-red-500 focus:border-red-500'
                  : 'focus:ring-blue-500 focus:border-blue-500'
              "
              required
              @blur="v$.password.$touch()"
            />
            <button
              class="absolute right-2 top-2 z-10"
              @click="showPassword = !showPassword"
            >
              <font-awesome-icon
                :icon="showPassword ? ['far', 'eye'] : ['far', 'eye-slash']"
                color="white"
              />
            </button>
          </div>
          <span
            class="text-sm"
            :class="v$.password.$error ? 'text-red-500' : ''"
            >{{ v$.password.$dirty ? (v$.password as any).required.$invalid ? 'La contraseña es requerida' : '&nbsp;' : '&nbsp;' }}</span
          >
        </div>
        <button
          type="submit"
          class="w-full focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800"
          :disabled="isSubmitting"
        >
          <loading-spinner v-if="isSubmitting" />
          <span v-else>Iniciar sesión</span>
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: opacity 0.25s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
}
</style>
