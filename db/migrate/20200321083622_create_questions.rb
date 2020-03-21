class CreateQuestions < ActiveRecord::Migration[6.0]
  def change
    create_table :questions do |t|
      t.integer :tag
      t.string :text

      t.timestamps
    end
  end
end
