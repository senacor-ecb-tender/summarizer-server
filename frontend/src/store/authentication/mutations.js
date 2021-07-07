import { Notify } from 'quasar'

export function auth_success(state, token, user) {
  state.status = 'success'
}

export function auth_error(state){
  Notify.create({
    message: 'Login failed due to wrong credentials or all summarisation pods are busy',
    type: 'negative'
  })
  state.status = 'error'
}

export function auth_error_other(state){
  Notify.create({
    message: 'Login failed as all summarisation pods are busy',
    type: 'negative'
  })
  state.status = 'error'
}

export function logout(state){
  state.status = ''
}
