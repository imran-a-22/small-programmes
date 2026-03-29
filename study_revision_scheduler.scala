// study_revision_scheduler.scala
// Creates a simple revision plan using day intervals.

import scala.io.StdIn.readLine

object StudyRevisionScheduler {
  def main(args: Array[String]): Unit = {
    println("Study Revision Scheduler")
    print("Enter topic name: ")
    val topic = readLine()

    print("Enter the day number you start on: ")
    val startDay = readLine().toIntOption

    if (startDay.isEmpty) {
      println("Please enter a valid whole number for the start day.")
      return
    }

    val intervals = List(0, 1, 3, 7, 14, 30)
    println(s"\nRevision plan for: $topic")

    intervals.zipWithIndex.foreach { case (offset, index) =>
      println(s"Session ${index + 1}: Day ${startDay.get + offset}")
    }

    println("\nTip: after each session, rate your confidence from 1 to 5.")
  }
}
