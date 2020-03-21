# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)

puts 'Cleaning database...'
Answer.destroy_all
Question.destroy_all

puts 'Starts Seeding...'
# __________________________________________________________________________User
puts '   Creating Questions'

Question.create!({
  tag: 1,
  text: 'Hier ist die erste Frage'
})
Question.create!({
  tag: 2,
  text: 'Hier ist die zweite Frage'
})
Question.create!({
  tag: 3,
  text: 'Hier ist die dritte Frage'
})

puts '   Creating Answers'

Answer.create!({
  question: Question.find_by(tag: 1),
  text: 'Antwort 1',
  next_question_tag: 2
})

Answer.create!({
  question: Question.find_by(tag: 1),
  text: 'Antwort 2',
  next_question_tag: 3
})

Answer.create!({
  question: Question.find_by(tag: 2),
  text: 'abc',
  next_question_tag: 2
})

Answer.create!({
  question: Question.find_by(tag: 2),
  text: 'xyz',
  next_question_tag: 3
})

Answer.create!({
  question: Question.find_by(tag: 3),
  text: '123',
  next_question_tag: 3
})

Answer.create!({
  question: Question.find_by(tag: 3),
  text: '345',
  next_question_tag: 3
})
