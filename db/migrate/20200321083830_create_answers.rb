class CreateAnswers < ActiveRecord::Migration[6.0]
  def change
    create_table :answers do |t|
      t.string :text
      t.integer :link_question
      t.references :question, null: false, foreign_key: true

      t.timestamps
    end
  end
end
