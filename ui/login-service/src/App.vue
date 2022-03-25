<script setup lang="ts">
import useVuelidate from '@vuelidate/core';
import LoadingSpinner from './components/LoadingSpinner.vue';
import { required, email } from '@vuelidate/validators';
import { ref } from 'vue';
import ky from 'ky';

const form = ref({
  email: '',
  password: '',
});
const showPassword = ref(false);
const isSubmitting = ref(false);

const rules: any = {
  email: { required, email },
  password: { required },
};

const v$ = useVuelidate(rules, form);

const handleSubmit = async () => {
  isSubmitting.value = true;
  if (!(await v$.value.$validate())) return;
  const res = await ky
    .post((import.meta.env['VITE_API_URL'] as string) + '/login', {
      headers: {
        Authorization:
          'Basic ' + btoa(form.value.email + ':' + form.value.password),
      },
    })
    .json();
  isSubmitting.value = false;
};
</script>

<template>
  <div class="pt-24">
    <div
      class="flex mx-auto max-w-4xl bg-white rounded-lg border border-gray-200 shadow-md dark:bg-gray-800 dark:border-gray-700"
    >
      <img
        src="./assets/farm_picture.jpg"
        class="object-cover w-full h-96 rounded-t-lg md:h-auto md:w-72 hidden md:block md:rounded-none md:rounded-l-lg"
      />
      <form
        class="space-y-6 px-6 py-12 flex-grow"
        @submit.prevent="handleSubmit"
      >
        <div class="flex justify-evenly items-center divide-x">
          <h5 class="text-xl font-medium text-gray-900 dark:text-white">
            Inicia Sesión
          </h5>
          <img src="./assets/evergreen.png" class="pl-8" />
        </div>
        <div>
          <label
            for="email"
            class="block text-sm font-medium text-gray-900 dark:text-gray-300"
            >Correo electrónico</label
          >
          <input
            v-model="form.email"
            type="email"
            name="email"
            id="email"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
            :class="
              v$.email.$error
                ? 'focus:ring-red-500 focus:border-red-500'
                : 'focus:ring-blue-500 focus:border-blue-500'
            "
            placeholder="nombre@evergreen.com"
            required
            @blur="v$.email.$touch()"
          />
          <span class="text-sm" :class="v$.email.$error ? 'text-red-500' : ''">
            {{ v$.email.$dirty ? (v$.email as any).required.$invalid ? 'El correo electrónico es requerido' : (v$.email as any).email.$invalid ? 'El correo electrónico no es válido' : '&nbsp;' : '&nbsp;' }}</span
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
          >
            {{ v$.password.$dirty ? (v$.password as any).required.$invalid ? 'La contraseña es requerida' : '&nbsp;' : '&nbsp;' }}
          </span>
        </div>
        <button
          type="submit"
          class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
          :disabled="isSubmitting"
        >
          <loading-spinner v-if="isSubmitting" />
          <span v-else>Iniciar sesión</span>
        </button>
      </form>
    </div>
  </div>
</template>
