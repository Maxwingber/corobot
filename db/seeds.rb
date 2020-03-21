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
  name: "eins",
  text: 'Hier ist die erste Frage'
})

puts '   Creating Answers'

Answer.create!({
  question: Question.find_by(name: "eins"),
  link_question: 1,
  text: 'Hier ist die erste Frage'
})
