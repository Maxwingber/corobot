Rails.application.routes.draw do
  root to: 'pages#home'

  resources :questions, only: [:index, :show]
end
