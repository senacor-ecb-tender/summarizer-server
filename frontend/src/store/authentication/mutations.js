import { Notify } from 'quasar'

export function auth_success(state, token, user) {
  state.status = 'success'
}

export function auth_error(state){
  Notify.create({
    message: 'Login failed!',
    type: 'negative'
  })
  state.status = 'error'
}

export function logout(state){
  state.status = ''
}
